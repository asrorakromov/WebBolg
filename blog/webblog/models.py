from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фотография')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='Видео')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)

    def time_ago(self):
        now = timezone.now()
        difference = now - self.created_at

        seconds = difference.total_seconds()
        if seconds < 60:
            return f"{int(seconds)} секунд назад"
        elif seconds < 3600:
            return f"{int(seconds // 60)} минут назад"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} часов назад"
        else:
            return f"{int(seconds // 86400)} дней назад"

    def edited_ago(self):
        now = timezone.now()
        difference = now - self.created_at

        seconds = difference.total_seconds()
        if seconds < 60:
            return f"изменено {int(seconds)} секунд назад"
        elif seconds < 3600:
            return f"изменено {int(seconds // 60)} минут назад"
        elif seconds < 86400:
            return f"изменено {int(seconds // 3600)} часов назад"
        else:
            return f"изменено {int(seconds // 86400)} дней назад"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://stroy-beton.com/wa-data/public/shop/products/19/71/87119/images/110288/110288.970.png'

    def get_absolute_url(self):
        return reverse('movie', kwargs={'pk': self.pk})

    def get_views(self):
        if self.views:
            return self.views.count()
        else:
            return 0


class Comments(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Видео')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def time_ago(self):
        now = timezone.now()
        difference = now - self.created_at

        seconds = difference.total_seconds()
        if seconds < 60:
            return f"{int(seconds)} секунд назад"
        elif seconds < 3600:
            return f"{int(seconds // 60)} минут назад"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} часов назад"
        else:
            return f"{int(seconds // 86400)} дней назад"

    def edited_ago(self):
        now = timezone.now()
        difference = now - self.created_at

        seconds = difference.total_seconds()
        if seconds < 60:
            return f"изменено {int(seconds)} секунд назад"
        elif seconds < 3600:
            return f"изменено {int(seconds // 60)} минут назад"
        elif seconds < 86400:
            return f"изменено {int(seconds // 3600)} часов назад"
        else:
            return f"изменено {int(seconds // 86400)} дней назад"

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        return reverse('comment_update', kwargs={'pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Аватарка')
    bio = models.CharField(max_length=200, blank=True, null=True, verbose_name=' О себе')
    publisher = models.BooleanField(default=True, verbose_name='Право добавления контента')

    def __str__(self):
        return self.user.username

    def get_photo_profile(self):
        try:
            return self.photo.url
        except:
            return 'https://shkolafominskaya-r22.gosweb.gosuslugi.ru/netcat_files/177/2753/pustoe_foto_0.jpg'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Ip(models.Model):
    ip = models.CharField(max_length=100, verbose_name='API адрес')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Видео', related_name='views')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'API адрес'
        verbose_name_plural = 'API адреса'
