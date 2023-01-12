from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'title', 'description', 'created_at')