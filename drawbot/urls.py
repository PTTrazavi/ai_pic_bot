from django.urls import path
from . import views
urlpatterns = [
    path('uploadImgDraw/', views.uploadImgDraw, name='upload_img_draw'),
    path('resultDraw/', views.resultDraw, name='result_draw'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
