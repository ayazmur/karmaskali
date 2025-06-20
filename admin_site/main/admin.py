from django.contrib import admin
from .models import Employee, News
from django.utils.html import format_html

admin.site.register(Employee)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'display_image')
    readonly_fields = ('display_image',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "—"

    display_image.short_description = 'Превью'