from PIL import Image
from google_images_download import google_images_download
import sys
import requests
from io import BytesIO
import time
from django.core.files.base import ContentFile
from .models import Imageupload
#add frame to the image
def imgtool(img_name, img_name_pre = False):
    #get file name and extension
    f_n = img_name.split("/")[-1].split(".")[0]
    f_e = img_name.split(".")[-1]
    #remove special charactor
    tbd = ['!','@','#','$','%','^','&','*','(',')','-','+','=']
    for i in tbd:
        f_n = f_n.replace(i,'')
    #if the extension is too long make it .jpg
    if len(f_e) > 7:
        f_e = "jpg"
    out_f_name = f_n + "_out." + f_e
    #Load the input image
    if "http" in img_name: # for GCS
        response = requests.get(img_name)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(img_name)
    #image process starts here
    width = 25
    # load pixels of pictures
    px = img.load()
    for x in range(0,img.size[0]):
        for y in range(0,img.size[1]):
            # add blue frame here
            if x < width or y < width or x > img.size[0] - width or y > img.size[1] - width :
                px[x,y] = 129, 216, 208 ,255

    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), out_f_name)
    img2 = Imageupload(image_file=img_content, title= out_f_name.split('.')[-2])
    img2.save()

    if img_name_pre is not False:
        #make preview image
        img = img.resize((200, int(200*img.size[1]/img.size[0])))
        #same process as above
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        pre_f_name = f_n + "_pre." + f_e
        img_content = ContentFile(img_io.getvalue(), pre_f_name)
        img3 = Imageupload(image_file=img_content, title= pre_f_name.split('.')[-2])
        img3.save()
        return (img2.image_file.url, img3.image_file.url)
    return img2.image_file.url

#google image search
def google_image(keyword, num=12, no_download=True):
    response = google_images_download.googleimagesdownload()
    #if keyword is empty:
    if keyword == "":
        keyword = "empty"
    data = response.download({
        "keywords": keyword,
        "color_type": "full-color",
        "format": "jpg",
        "size": "icon",
        "limit": num,
        'no_directory': True,
        'no_download': no_download,
        'silent_mode': True,
        "output_directory": "media/images/",})
    data = data[0][keyword]
    #return data
    #make sure each url is ok
    urls = []
    for u in data:
        if str(u).startswith('http'):
            urls.append(u)
    return urls

import requests
import pandas as pd
import urllib.request
def flickr_image(keyword, num=12, download=False):
    url_flickr = "https://www.flickr.com/"
    data_flickr = requests.get(url_flickr)
    api_key = str(data_flickr.content).split("api.site_key")[1]
    api_key = api_key.split('"')[1]
    url = "https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias%2Crealname%2Crotation%2Curl_m&per_page=" + str(num) +"&page=1&lang=zh-Hant-HK&text=" + keyword + "&viewerNSID=&method=flickr.photos.search&csrf=&api_key=" + api_key + "&format=json&hermes=1&hermesClient=1&reqId=3405dc98&nojsoncallback=1"
    data = requests.get(url)
    data = data.json()
    data = pd.DataFrame.from_dict(data['photos']['photo'])
    data = data.filter(["height_m", "width_m", "url_m"])
    data = data.fillna(0)
    data['height_m'] = data['height_m'].astype(int)
    data['width_m'] = data['width_m'].astype(int)
    data = data[data['height_m'] <= 500]
    data = data[data['width_m'] <= 500]
    if download:
        for i in range(len(data)):
            urllib.request.urlretrieve(data.url_m[i], "media/images/" + str(i+1) + ". " +data.url_m[i].split("/")[-1])
    #return list(data.url_m)
    #make sure each url is ok
    urls = []
    for u in list(data.url_m):
        if str(u).startswith('http'):
            urls.append(u)
    return urls

from .deepllabv3plus import *
def seg_img(photo_input):
    photo_out = run_deeplabv3plus(photo_input)
    return photo_out
