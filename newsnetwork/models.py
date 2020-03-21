from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PostModel(models.Model):
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