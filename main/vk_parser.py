from datetime import datetime

import requests
import json
from .models import News, NewsImage
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os
from django.conf import settings


def download_image(url, news_instance):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Создаем имя файла из URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # Сохраняем изображение
        image_file = ContentFile(response.content)
        news_image = NewsImage(news=news_instance)
        news_image.image.save(filename, image_file, save=True)
        return news_image
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return None


def parse_vk_posts(group_id, count=5):
    # Ваш API ключ VK
    ACCESS_TOKEN = 'YOUR_VK_API_TOKEN'
    VERSION = '5.131'

    try:
        # Получаем посты из группы
        response = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'owner_id': f'-{group_id}',
                'count': count,
                'access_token': ACCESS_TOKEN,
                'v': VERSION,
                'extended': 1
            }
        )

        data = response.json()

        if 'response' not in data:
            print("Error in VK API response:", data)
            return False

        posts = data['response']['items']

        for post in posts:
            # Проверяем, есть ли уже такой пост
            if News.objects.filter(vk_post_id=post['id']).exists():
                continue

            # Создаем новость
            news = News(
                title=post['text'][:200] if post['text'] else 'Новость из VK',
                content=post['text'],
                date=datetime.fromtimestamp(post['date']),
                vk_post_id=post['id'],
                vk_group_id=group_id
            )
            news.save()

            # Обрабатываем вложения (фото)
            if 'attachments' in post:
                for attachment in post['attachments']:
                    if attachment['type'] == 'photo':
                        # Берем фото максимального размера
                        photo_url = attachment['photo']['sizes'][-1]['url']
                        download_image(photo_url, news)

        return True
    except Exception as e:
        print(f"Error parsing VK posts: {e}")
        return False