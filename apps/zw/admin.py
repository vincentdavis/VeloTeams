from django.contrib import admin
from .models import Profile, Club


@admin.register(Profile)
class ZwiftProfileAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(Club)
class ZwiftClubAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

