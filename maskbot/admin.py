from django.contrib import admin
from .models import Imageuploadmask, Keywordmask

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

@admin.register(Keywordmask)
class KeywordmaskAdmin(admin.ModelAdmin):
    list_display = ('date_of_search', 'keyword')

@admin.register(Imageuploadmask)
class ImageuploadmaskAdmin(admin.ModelAdmin):
    list_display = ('date_of_upload', 'title', 'image_file')
