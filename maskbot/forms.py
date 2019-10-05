from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class GoogleForm(forms.Form):
    keyword = forms.CharField(required=False, label="關鍵字", label_suffix=":")
    size = forms.IntegerField(required=True, label="外擴參數", label_suffix=":", initial=5, min_value=0, max_value=20,
                                widget=forms.NumberInput(attrs={'type':'range','step':1,'onchange':'updateText(this.value);'}))
    #temp is only for display of size
    temp = forms.IntegerField(label="", label_suffix="", initial=5,
                                widget=forms.NumberInput(attrs={'readonly':True}))

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
    size = forms.IntegerField(required=True, label="外擴參數", label_suffix=":", initial=5, min_value=0, max_value=20,
                                widget=forms.NumberInput(attrs={'type':'range','step':1,'onchange':'updateText(this.value);'}))
    #temp is only for display of size
    temp = forms.IntegerField(label="", label_suffix="", initial=5,
                                widget=forms.NumberInput(attrs={'readonly':True}))

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
    image = forms.ImageField(label="圖片檔案", label_suffix=":")
    size = forms.IntegerField(required=True, label="外擴參數", label_suffix=":", initial=5, min_value=0, max_value=20,
                                widget=forms.NumberInput(attrs={'type':'range','step':1,'onchange':'updateText(this.value);'}))
    #temp is only for display of size
    temp = forms.IntegerField(label="", label_suffix="", initial=5,
                                widget=forms.NumberInput(attrs={'readonly':True}))
                                
    def clean_image(self):
        data = self.cleaned_data['image']
        return data

    def clean_size(self):
        data = self.cleaned_data['size']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Size should be positive integer!"))
        return data
