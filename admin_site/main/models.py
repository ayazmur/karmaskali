from django.db import models
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
    image = models.ImageField(upload_to='news/images/')
    is_featured = models.BooleanField(default=False, verbose_name='Главное изображение')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Изображение для {self.news.title}"

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = RichTextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    def featured_image(self):
        # Возвращает главное изображение или первое, если не выбрано
        featured = self.images.filter(is_featured=True).first()
        return featured or self.images.first()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

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