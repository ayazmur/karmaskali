from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    image = models.ImageField('Главное изображение', upload_to='news/', blank=True, null=True)
    content = models.TextField('Текст новости')  # Можно использовать HTML-теги
    date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'