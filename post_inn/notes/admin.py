from django.contrib import admin
from .models import Note, Tag


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'update', 'is_active', 'is_favorites']
    list_filter = ('author',)
    # raw_id_fields = ('tags',)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'update']
    list_filter = ('author',)
