import os
import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        ordering = ['-created_at']


def image_upload_to(isinstance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(isinstance.UPLOAD_PATH, "%s.%s" %(uuid.uuid4(), ext))


class Image(BaseModel):
    UPLOAD_PATH = 'user-upload' # 내가 정한 경로임(/gram/media)

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() #image numbering

    class Meta:
        unique_together = ['content', 'order']
        ordering = ['order']


class FollowRelation(BaseModel):
    follower = models.OneToOneField(User, on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='followee')