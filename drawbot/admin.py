from django.contrib import admin
from .models import Imageuploaddraw

@admin.register(Imageuploaddraw)
class ImageuploaddrawAdmin(admin.ModelAdmin):
    list_display = ('date_of_upload', 'title', 'image_file')
