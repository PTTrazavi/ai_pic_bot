from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UploadimgdrawForm(forms.Form):
    image = forms.ImageField(label="", label_suffix="")

    def clean_image(self):
        data = self.cleaned_data['image']

        # Remember to always return the cleaned data.
        return data
