from django.db import models
from PIL import Image
from django.contrib.auth.models import User


class CMVData(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    cmv = models.IntegerField(blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    stri = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.id


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default=r'C:\Users\ajinf\PycharmProjects\Maps\media\default.jpg',
                               upload_to=r'C:\Users\ajinf\PycharmProjects\Maps\media\profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
