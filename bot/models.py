from django.db import models
from django.core.files import File
import os

class Imageupload(models.Model):
    title = models.TextField()
    image_file = models.ImageField(upload_to='images/')
    date_of_upload = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Keyword(models.Model):
    """Model representing a keyword."""
    keyword = models.CharField(max_length=100)
    date_of_search = models.DateTimeField(null=True, blank=True)

    #def get_absolute_url(self):
    #    """Returns the url to access a particular keyword instance."""
    #    return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.keyword}, {self.date_of_search}'
