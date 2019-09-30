from django.shortcuts import render, get_object_or_404
import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os
import time, datetime
from PIL import Image
from base64 import b64decode
from io import BytesIO
from django.core.files.base import ContentFile
import requests
from .util import imgtool_draw #, google_image_draw, flickr_image_draw
from django.views.generic import ListView

# upload image
from .models import Imageuploaddraw
from .forms import UploadimgdrawForm
def uploadImgDraw(request):
    logging.error('Someone visited uploadImgDraw of drawbot...')

    if request.method == 'POST':
        form = UploadimgdrawForm(request.POST, request.FILES) #remember to add request.FILES!
        # Check if the form is valid:
        if form.is_valid():
            filename = str(int(time.time()))
            image_by_user = form.cleaned_data['image']
            date_of_upload = str(datetime.datetime.today())
            img = Imageuploaddraw(image_file=image_by_user, title=filename, date_of_upload = date_of_upload)
            img.save()
            #get width height and make canvas size, default width 500
            img_w = img.image_file.width
            img_h = img.image_file.height
            ratio = img_h/img_w
            if img_w > 500:
                img_w = 500
                img_h = 500 * ratio

            content = {
                'form': form,
                'original': img.image_file.url[:],
                'pk': img.pk,
                'img_w': img_w,
                'img_h': img_h,
            }
            return render(request, 'drawbot/uploadImgDraw.html', content)
    # If this is a GET (or any other method) create the default form.
    else:
        form = UploadimgdrawForm()
    # default or not valid comes here
    content = {
        'form': form,
    }
    return render(request, 'drawbot/uploadImgDraw.html',content)


def resultDraw(request):
    logging.error('Someone visited result of drawbot...')

    if request.method == 'POST':
        #trimap image
        canvasData = request.POST.get('canvasData')
        format, imgstr = canvasData.split(';base64,')
        ext = format.split('/')[-1]
        filename = str(int(time.time())) + "." + "jpg" #"jpg" ext
        img_content = ContentFile(b64decode(imgstr),filename)
        date_of_upload = str(datetime.datetime.today())
        img_t = Imageuploaddraw(image_file=img_content, title=filename, date_of_upload = date_of_upload)
        img_t.save()
        #original image
        pk = request.POST.get('pk')
        img_o = get_object_or_404(Imageuploaddraw, pk=pk)
        #process the image to make some changes
        #see if the file is local or on GCS
        if 'http' in img_o.image_file.url:
            img_out = imgtool_draw(img_o.image_file.url[:]) #GCS
            #img_out = seg_img_draw(img_o.image_file.url[:]) #GCS
        else:
            img_out = imgtool_draw(img_o.image_file.url[1:])
            #img_out = seg_img_draw(img_o.image_file.url[1:])

        content = {
                'img_org': img_o.image_file.url[:],
                'img_tri': img_t.image_file.url[:],
                'img_ai': img_out,
        }

        return render(request, 'drawbot/resultDraw.html', content)
