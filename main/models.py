

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Employee(models.Model):
    name = models.CharField('ФИО', max_length=100)
    position = models.CharField('Должность', max_length=100)
    photo = models.ImageField('Фото', upload_to='employees/', blank=True, null=True)
    phone = models.CharField('Рабочий телефон', max_length=20, blank=True)
    bio = models.TextField('Биография', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class NewsImage(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='news/images/')
    is_featured = models.BooleanField('Главное изображение', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение новости'
        verbose_name_plural = 'Изображения новостей'

    def __str__(self):
        return f"Изображение для {self.news.title}"


class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст новости')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    date = models.DateTimeField('Дата публикации', default=timezone.now)
    # существующие поля
    vk_post_id = models.CharField('ID поста VK', max_length=100, blank=True, null=True, unique=True)
    vk_group_id = models.CharField('ID группы VK', max_length=100, blank=True, null=True)
    def __str__(self):
        return self.title

    def featured_image(self):
        """Возвращает главное изображение или первое, если не выбрано"""
        featured = self.images.filter(is_featured=True).first()
        return featured or self.images.first()

    def get_local_date(self):
        """Возвращает дату в Уфимском времени (UTC+5)"""
        return timezone.localtime(self.date).strftime('%d.%m.%Y %H:%M')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

class Gallery(models.Model):
    title = models.CharField('Название', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'

    def __str__(self):
        return self.title or f"Галерея #{self.id}"

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='gallery/')
    title = models.CharField('Название', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Изображения галереи'

    def __str__(self):
        return self.title or f"Изображение #{self.id}"