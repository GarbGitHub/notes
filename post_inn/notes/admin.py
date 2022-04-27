from django.contrib import admin
from .models import Note, Tag


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'update', 'author', 'is_active', 'is_favorites',]


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'is_active', 'created', 'update']
    ordering = ['-is_active']