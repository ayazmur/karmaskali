from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('employees/', views.employees, name='employees'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
]