# Generated by Django 2.2.4 on 2019-09-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_remove_imageupload_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='date_of_search',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]