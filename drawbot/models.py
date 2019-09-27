from django.db import models
from django.core.files import File
import os

class Imageuploaddraw(models.Model):
    title = models.TextField()
    image_file = models.ImageField(upload_to='images/')
    date_of_upload = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
