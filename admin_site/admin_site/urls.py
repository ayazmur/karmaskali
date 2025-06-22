import subprocess

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        try:
            # Запускаем скрипт обновления
            subprocess.run(["/home/ayazmur/auto-update.sh"], check=True)
            return HttpResponse("Сайт успешно обновлен!", status=200)
        except Exception as e:
            return HttpResponse(f"Ошибка: {e}", status=500)
    return HttpResponse("Только POST-запросы разрешены", status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('webhook/', github_webhook),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)