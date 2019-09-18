from django.urls import include, path
from . import views
from .views import uploadImg


# 用來串接callback主程式
urlpatterns = [
    path('callback/', views.callback),
    path('google/', views.webgoogle, name='web_google'),
    path('flickr/', views.webflickr, name='web_flickr'),
    path('uploadImg/', uploadImg, name='upload_img'),
    path('result/', views.result, name='result'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
