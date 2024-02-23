import imp
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Video(models.Model):
    caption = models.CharField(max_length=100, blank=False, null=True)
    url = models.URLField(max_length=255, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    subtitle = models.FileField(null=True,blank=True, upload_to='subtitles')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.caption

class Streamer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    url = models.URLField(max_length=255,blank=True,null=True,default='') 

    def __str__(self):
        return self.user.username