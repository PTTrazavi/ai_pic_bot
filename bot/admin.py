from django.contrib import admin
from .models import Imageupload, Keyword

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('date_of_search', 'keyword')

@admin.register(Imageupload)
class ImageuploadAdmin(admin.ModelAdmin):
    list_display = ('date_of_upload', 'title', 'image_file')
