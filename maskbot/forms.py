from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class GoogleForm(forms.Form):
    keyword = forms.CharField(required=False, label="關鍵字", label_suffix=":")
    size = forms.IntegerField(required=True, label="外擴", label_suffix=":", initial=5,
                                help_text="外擴灰色地帶參數，輸入正的整數")

    def clean_keyword(self):
        data = self.cleaned_data['keyword']
        # Check if a date is not in the past.
        if len(data) < 1 :
            raise ValidationError(_("Keyword can't be empty!"))
        # Remember to always return the cleaned data.
        return data

    def clean_size(self):
        data = self.cleaned_data['size']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Size should be positive integer!"))
        return data

class FlickrForm(forms.Form):
    keyword = forms.CharField(required=False, label="關鍵字", label_suffix=":")
    size = forms.IntegerField(required=True, label="外擴", label_suffix=":", initial=5,
                                help_text="外擴灰色地帶參數，輸入正的整數")

    def clean_keyword(self):
        data = self.cleaned_data['keyword']
        # Check if a date is not in the past.
        if len(data) < 1 :
            raise ValidationError(_("Please enter something to search!"))
        # Remember to always return the cleaned data.
        return data

    def clean_size(self):
        data = self.cleaned_data['size']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Size should be positive integer!"))
        return data

class UploadimgForm(forms.Form):
    image = forms.ImageField(label="圖片", label_suffix=":")
    size = forms.IntegerField(required=True, label="外擴", label_suffix=":", initial=5,
                                help_text="外擴灰色地帶參數，輸入正的整數")

    def clean_image(self):
        data = self.cleaned_data['image']
        return data

    def clean_size(self):
        data = self.cleaned_data['size']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Size should be positive integer!"))
        return data
