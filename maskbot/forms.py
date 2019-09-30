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

        # Remember to always return the cleaned data.
        return data
