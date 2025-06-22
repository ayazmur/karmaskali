from django.contrib import admin
from django import forms
from django.http import JsonResponse
from django.utils.html import format_html
from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .models import Employee, News, NewsImage
from django.db.models import Count
import os
from django.conf import settings


# Множественная загрузка изображений
class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_image_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_image_clean(d, initial) for d in data]
        return [single_image_clean(data, initial)]


class NewsImageForm(forms.ModelForm):
    images = MultipleImageField(required=False, label='Добавить несколько изображений')

    class Meta:
        model = NewsImage
        fields = '__all__'


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    form = NewsImageForm
    extra = 0
    fields = ('image', 'is_featured', 'caption', 'order', 'preview')
    readonly_fields = ('preview',)
    ordering = ('order',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "—"

    preview.short_description = 'Превью'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display_featured_image', 'image_count')
    inlines = [NewsImageInline]
    change_form_template = 'admin/news_change_form.html'

    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = 'Изображения'

    def display_featured_image(self, obj):
        featured = obj.featured_image()
        if featured:
            return format_html('<img src="{}" width="150" />', featured.image.url)
        return "—"

    display_featured_image.short_description = 'Главное изображение'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-images/<int:news_id>/', self.upload_images, name='upload_images'),
            path('update-image-order/', self.update_image_order, name='update_image_order'),
        ]
        return custom_urls + urls

    def upload_images(self, request, news_id):
        if news_id == 'add':
            # Если новость еще не создана, сохраняем ее сначала
            if request.method == 'POST':
                form = self.get_form(request)(request.POST, request.FILES)
                if form.is_valid():
                    news = form.save()
                    images = request.FILES.getlist('images')
                    for image in images:
                        NewsImage.objects.create(news=news, image=image)
                    return redirect(f'../{news.id}/')
            else:
                return redirect('../')  # Возвращаем к форме создания новости

        # Остальной код обработки для существующей новости
        news = News.objects.get(id=news_id)
        if request.method == 'POST':
            images = request.FILES.getlist('images')
            for image in images:
                NewsImage.objects.create(news=news, image=image)
            return redirect(f'../{news_id}/')

        context = {
            **self.admin_site.each_context(request),
            'news_id': news_id,
            'opts': self.model._meta,
        }
        return TemplateResponse(request, 'admin/upload_images.html', context)

    def update_image_order(self, request):
        if request.method == 'POST':
            order_data = request.POST.getlist('order[]')
            for i, image_id in enumerate(order_data):
                NewsImage.objects.filter(id=image_id).update(order=i)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'photo_preview')
    list_display_links = ('name',)
    search_fields = ('name', 'position')
    fields = ('name', 'position', 'phone', 'photo', 'bio')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.photo.url)
        return "—"
    photo_preview.short_description = 'Фото'