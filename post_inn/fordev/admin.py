from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page, PageCategory


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('text', 'description',)  # визуальный редактор
    list_display = ['title', 'category', 'created', 'update', 'is_active']
    ordering = ['-is_active']


@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created', 'update']
    ordering = ['-is_active']
