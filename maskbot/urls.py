from django.urls import include, path
from . import views

# 用來串接callback主程式
urlpatterns = [
    path('callbackMask/', views.callbackMask),
    path('googleMask/', views.webgoogleMask, name='web_google_mask'),
    path('flickrMask/', views.webflickrMask, name='web_flickr_mask'),
    path('uploadImgMask/', views.uploadImgMask, name='upload_img_mask'),
    path('resultMask/', views.resultMask, name='result_mask'),
    path('combineAppMask/', views.combineAppMask, name='combine_app_mask'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
