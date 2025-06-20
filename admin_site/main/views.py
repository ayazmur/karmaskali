from django.shortcuts import render
from .models import Employee, News

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

def contact(request):
    if request.method == 'POST':
        # Обработка формы (можно добавить сохранение в БД или отправку на почту)
        pass
    return render(request, 'contact.html')