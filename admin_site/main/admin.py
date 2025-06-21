from django.contrib import admin
from .models import Employee, News, NewsImage
from django.utils.html import format_html

admin.site.register(Employee)

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image', 'is_featured', 'caption')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "—"
    preview.short_description = 'Превью'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display_featured_image')
    inlines = [NewsImageInline]

    def display_featured_image(self, obj):
        featured = obj.featured_image()
        if featured:
            return format_html('<img src="{}" width="150" />', featured.image.url)
        return "—"
    display_featured_image.short_description = 'Главное изображение'