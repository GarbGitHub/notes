from django.contrib import admin
from .models import Page, PageCategory


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'description', 'text', 'created', 'update', 'is_active']
    ordering = ['-is_active']


@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created', 'update']
    ordering = ['-is_active']
