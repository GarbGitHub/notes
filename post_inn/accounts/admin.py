from django.contrib import admin
from .models import User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'staff', 'is_active', 'admin', 'timestamp']
    ordering = ['-is_active', '-admin', 'staff', ]