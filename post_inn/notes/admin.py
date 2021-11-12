from django.contrib import admin
from .models import Note


# admin.site.register(Note)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'full_text', 'created', 'update', 'author']
