from django.db import models
from phone_field import PhoneField
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=35)
    phone = PhoneField()
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.name

class Request(models.Model):
    choice = (('Yes','Yes'), ('No','No'))
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=35)
    phone = PhoneField()
    category = models.CharField(max_length=7)
    topic = models.TextField(max_length=400)
    approved = models.CharField(max_length=3, choices=choice, blank=True, null=True)


    def __str__(self):
        return self.name

class Newsletter(models.Model):
    email = models.EmailField(max_length=35)

    def __str__(self):
        return self.email

class Post(models.Model):
    choice = (('Yes','Yes'), ('No','No'))
    title = models.CharField(max_length=75, blank=False, null=False)
    category = models.CharField(max_length=7)
    user = models.CharField(max_length=15)
    date = models.DateField(blank=True, null=True)
    featured_image = models.FileField(upload_to="Image")
    body = RichTextField()
    approved = models.CharField(max_length=3, choices=choice, blank=True, null=True)
    featured = models.CharField(max_length=3, choices=choice, blank=True, null=True,)
    auto_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)

    def __str__(self):
        return self.title

