from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

class NewsImage(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/images/')
    is_featured = models.BooleanField(default=False, verbose_name='Главное изображение')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись')

    def __str__(self):
        return f"Изображение для {self.news.title}"

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст новости')  # Можно использовать HTML-теги
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