from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageMessage,
    ImageSendMessage,
)
import os
import time, datetime
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import requests
from .util import imgtool, google_image, flickr_image, seg_img2, seg_matting
from django.views.generic import ListView
#parameter for global count
count = 0

YOUR_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
YOUR_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    signature = request.META["HTTP_X_LINE_SIGNATURE"]
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)

# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    #save user provided image in the folder, max 3 images
    global count
    if count == 5:
        count = 0
    count = count + 1
    #image saving code here
    with open("media/images/test" + str(count) + ".jpg", 'wb') as fd:
        for chunk in line_bot_api.get_message_content(event.message.id).iter_content():
            fd.write(chunk)
    #process the image to make some changes
    img_out, img_pre = imgtool("media/images/test" + str(count) + ".jpg", True)
    #img_out = seg_img("media/images/test" + str(count) + ".jpg")
    #send back the message id (used for debug)
    image_message1 = TextSendMessage(text=str(line_bot_api.get_message_content(event.message.id)) + "AI處理圖片中請稍等10~15秒")
    #send back the original image sent by the user
    image_message2 = ImageSendMessage(
                                    original_content_url='https://c518e079.ngrok.io' + img_out,
                                    preview_image_url='https://c518e079.ngrok.io' + img_out
                                )
    #line_bot_api.reply_message(event.reply_token, image_message1)
    line_bot_api.reply_message(event.reply_token, image_message2)

#google
from .models import Keyword
from .forms import GoogleForm
def webgoogle(request):
    if request.method == 'POST':
        form = GoogleForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            date_of_search = str(datetime.datetime.today())
            word_to_search = form.cleaned_data['keyword']
            key = Keyword(keyword = word_to_search, date_of_search = date_of_search)
            key.save()
            urls = google_image(word_to_search)
            content = {
                'form': form,
                'keyword': word_to_search,
                'url_0': urls[0],
                'url_1': urls[1],
                'url_2': urls[2],
                'url_3': urls[3],
                'url_4': urls[4],
                'url_5': urls[5],
                'url_6': urls[6],
                'url_7': urls[7],
                'url_8': urls[8],
            }
            return render(request, 'bot/webgoogle.html', content)
    # If this is a GET (or any other method) create the default form.
    else:
        form = GoogleForm()
    # default or not valid comes here
    content = {
        'form': form,
    }
    return render(request, 'bot/webgoogle.html', content)

#flickr
from .forms import FlickrForm
def webflickr(request):
    if request.method == 'POST':
        form = FlickrForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            date_of_search = str(datetime.datetime.today())
            word_to_search = form.cleaned_data['keyword']
            key = Keyword(keyword = word_to_search, date_of_search = date_of_search)
            key.save()
            urls = flickr_image(word_to_search)
            content = {
                'form': form,
                'keyword': word_to_search,
                'url_0': urls[0],
                'url_1': urls[1],
                'url_2': urls[2],
                'url_3': urls[3],
                'url_4': urls[4],
                'url_5': urls[5],
                'url_6': urls[6],
                'url_7': urls[7],
                'url_8': urls[8],
            }
            return render(request, 'bot/webflickr.html', content)
    # If this is a GET (or any other method) create the default form.
    else:
        form = FlickrForm()
    # default or not valid comes here
    content = {
        'form': form,
    }
    return render(request, 'bot/webflickr.html', content)

# upload image
from .models import Imageupload
from .forms import UploadimgForm
def uploadImg(request):
    form = UploadimgForm()
    # default or not valid comes here
    content = {
        'form': form,
    }
    return render(request, 'bot/uploadImg.html',content)

#show result
from .forms import MattingForm
def result(request_s):
    if request_s.POST.get('img_url'):
        url = request_s.POST.get('img_url')
        #get file name and extension
        f_n = url.split("/")[-1].split(".")[0]
        f_e = url.split(".")[-1]
        #remove special charactor
        tbd = ['!','@','#','$','%','^','&','*','(',')','-','+','=']
        for i in tbd:
            f_n = f_n.replace(i,'')
        #if the extension is too long make it .jpg
        if len(f_e) > 7:
            f_e = "jpg"
        #save the original image
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        out_f_name = f_n + "." + f_e
        img_content = ContentFile(img_io.getvalue(), out_f_name)
        date_of_upload = str(datetime.datetime.today())
        img = Imageupload(image_file=img_content, title= f_n, date_of_upload = date_of_upload )
        img.save()
        #process the image to make some changes
        #see if the file is local or on GCS
        if 'http' in img.image_file.url:
            #img_out = imgtool(img.image_file.url[:]) #GCS
            img_out = seg_img2(img.image_file.url[:]) #GCS
        else:
            #img_out = imgtool(img.image_file.url[1:])
            img_out = seg_img2(img.image_file.url[1:])

        #form prepare
        form = MattingForm(initial={'original':img.pk, 'mask':img_out[1]})

        content = {
                'img_org': img.image_file.url[:],
                'img_out': img_out[2],
                'form': form,
        }
        return render(request_s, 'bot/result.html', content)

    elif request_s.FILES:
        form = UploadimgForm(request_s.POST, request_s.FILES) #remember to add request.FILES!
        # Check if the form is valid:
        if form.is_valid():
            filename = str(int(time.time()))
            image_by_user = form.cleaned_data['image']
            date_of_upload = str(datetime.datetime.today())
            img = Imageupload(image_file=image_by_user, title=filename, date_of_upload = date_of_upload)
            img.save()
            #process the image to make some changes
            #see if the file is local or on GCS
            if 'http' in img.image_file.url:
                #img_out = imgtool(img.image_file.url[:]) #GCS
                img_out = seg_img2(img.image_file.url[:]) #GCS
            else:
                #img_out = imgtool(img.image_file.url[1:])
                img_out = seg_img2(img.image_file.url[1:])

            #form prepare
            form = MattingForm(initial={'original':img.pk, 'mask':img_out[1]})

            content = {
                    'img_org': img.image_file.url[:],
                    'img_out': img_out[2],
                    'form': form,
            }
            return render(request_s, 'bot/result.html', content)

    else:
        form = MattingForm(request_s.POST)
        # Check if the form is valid:
        if form.is_valid():
            #get original and mask images first
            pk_o = form.cleaned_data['original']
            pk_m = form.cleaned_data['mask']
            size = form.cleaned_data['size'] + 5 #get size parameter
            img_org = get_object_or_404(Imageupload, pk=pk_o)
        #process the image to make some changes
        img_out = seg_matting(pk_o, pk_m, size)
        #form prepare
        form = MattingForm(initial={'original':pk_o, 'mask':pk_m, 'size':size-5, 'temp': size-5})

        content = {
                'img_org': img_org.image_file.url[:],
                'trimap': img_out[0],
                'matting': img_out[1],
                'form': form,
        }
        return render(request_s, 'bot/result.html', content)

#Green screen combine app
def combineApp(request):

    return render(request, 'bot/combineApp.html')
