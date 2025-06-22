from django.shortcuts import render
from .models import Employee, News, Gallery


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def employees(request):
    employees_list = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees_list})

def news(request):
    news_list = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news': news_list})
def news_detail(request, news_id):
    news_item = News.objects.get(id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})
def contact(request):
    if request.method == 'POST':
        # Обработка формы (можно добавить сохранение в БД или отправку на почту)
        pass
    return render(request, 'contact.html')

def gallery(request):
    galleries = Gallery.objects.prefetch_related('images').all()
    return render(request, 'gallery.html', {'galleries': galleries})