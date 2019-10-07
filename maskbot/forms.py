from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class GoogleForm(forms.Form):
    keyword = forms.CharField(required=False, label="", label_suffix="")

    def clean_keyword(self):
        data = self.cleaned_data['keyword']
        # Check if a date is not in the past.
        if len(data) < 1 :
            raise ValidationError(_("Keyword can't be empty!"))
        # Remember to always return the cleaned data.
        return data

class FlickrForm(forms.Form):
    keyword = forms.CharField(required=False, label="", label_suffix="")

    def clean_keyword(self):
        data = self.cleaned_data['keyword']
        # Check if a date is not in the past.
        if len(data) < 1 :
            raise ValidationError(_("Please enter something to search!"))
        # Remember to always return the cleaned data.
        return data

class UploadimgForm(forms.Form):
    image = forms.ImageField(label="", label_suffix="")

    def clean_image(self):
        data = self.cleaned_data['image']
        return data

class MattingForm(forms.Form):
    original = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'type':'hidden'}))
    mask = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'type':'hidden'}))
    size = forms.IntegerField(required=True, label="外擴參數", label_suffix=":", initial=0, min_value=0, max_value=20,
                                widget=forms.NumberInput(attrs={'type':'range','step':1,'onchange':'updateText(this.value);'}))
    #temp is only for display of size
    temp = forms.IntegerField(label="", label_suffix="", initial=0,
                                widget=forms.NumberInput(attrs={'readonly':True}))

    def clean_original(self):
        data = self.cleaned_data['original']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Original should be positive integer!"))
        return data

    def clean_mask(self):
        data = self.cleaned_data['mask']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Mask should be positive integer!"))
        return data

    def clean_size(self):
        data = self.cleaned_data['size']
        # Check if size >= 0
        if data < 0 :
            raise ValidationError(_("Size should be positive integer!"))
        return data
