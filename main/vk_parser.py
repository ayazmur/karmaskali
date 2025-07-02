import requests
from django.utils import timezone
from .models import News, NewsImage, User
from django.conf import settings
from urllib.parse import urlparse
import os
from django.core.files import File
from tempfile import NamedTemporaryFile


def get_vk_news():
    # Получаем последние 10 постов из группы
    url = f"https://api.vk.com/method/wall.get?owner_id=-{settings.VK_GROUP_ID}&count=10&access_token={settings.VK_ACCESS_TOKEN}&v=5.131"

    try:
        response = requests.get(url)
        data = response.json()

        if 'response' in data:
            posts = data['response']['items']

            # Получаем или создаем пользователя для автора постов
            admin_user = User.objects.filter(is_superuser=True).first()

            for post in posts:
                # Пропускаем репосты и посты без текста
                if post.get('copy_history') or not post.get('text'):
                    continue

                # Проверяем, есть ли уже такая новость
                if not News.objects.filter(title=post['text'][:100]).exists():
                    # Создаем новость
                    news = News.objects.create(
                        title=post['text'][:200],  # Берем первые 200 символов как заголовок
                        content=post['text'],
                        author=admin_user,
                        date=timezone.datetime.fromtimestamp(post['date'])
                    )

                    # Обрабатываем вложения (фото)
                    if 'attachments' in post:
                        for attachment in post['attachments']:
                            if attachment['type'] == 'photo':
                                # Берем фото максимального размера
                                photo_url = attachment['photo']['sizes'][-1]['url']

                                # Скачиваем и сохраняем изображение
                                img_temp = NamedTemporaryFile(delete=True)
                                img_temp.write(requests.get(photo_url).content)
                                img_temp.flush()

                                img_name = os.path.basename(urlparse(photo_url).path)
                                news_image = NewsImage(news=news, image=File(img_temp, name=img_name))
                                news_image.save()

        return True
    except Exception as e:
        print(f"Ошибка при получении новостей из ВК: {e}")
        return False