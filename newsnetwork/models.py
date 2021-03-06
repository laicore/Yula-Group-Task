from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from os import remove as _rm

# Create your models here.


class PostModelManager(models.Manager):
    def new(self):
        posts = self.filter(moderated=True)
        return posts.order_by('-addedDatetime')

    def newID(self):
        posts = self.filter(moderated=True)
        return posts.order_by('-id')


class PostModel(models.Model):
    objects = PostModelManager()
    name = models.CharField(max_length=100, verbose_name='Название')
    text = models.CharField(max_length=2000, null=True,
                            verbose_name='Текст', blank=True)
    image = models.ImageField(
        null=True, verbose_name='Изображение', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    addedDatetime = models.DateTimeField(auto_now=True)
    moderated = models.BooleanField(default=False)

    def get_url(self):
        return "/post/"+str(self.id)

    class Meta:
        verbose_name = "Post"


@receiver(models.signals.post_delete, sender=PostModel)
def delete_file(instance, using, **kwargs):
    if instance.image.name is not '':
        _rm(instance.image.path)
        
    
