from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Employee, News, Gallery


def home(request):
    latest_news = News.objects.all().order_by('-date')[:5]
    return render(request, 'index.html', {'latest_news': latest_news})


def about(request):
    return render(request, 'about.html')


def employees(request):
    employees_list = Employee.objects.all()
    return render(request, 'employees/employees.html', {'employees': employees_list})


def news(request):
    news_list = News.objects.all().order_by('-date')

    # Добавляем поиск
    search_query = request.GET.get('q')
    if search_query:
        news_list = news_list.filter(title__icontains=search_query)

    # Добавляем пагинацию (10 новостей на страницу)
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })


def news_detail(request, news_id):
    news_item = get_object_or_404(News.objects.select_related('author'), id=news_id)
    return render(request, 'news/news_detail.html', {'news': news_item})


def contact(request):
    if request.method == 'POST':
        # Обработка формы (можно добавить сохранение в БД или отправку на почту)
        pass
    return render(request, 'contact.html')


def gallery(request):
    galleries = Gallery.objects.prefetch_related('images').all()
    return render(request, 'gallery/gallery.html', {'galleries': galleries})
