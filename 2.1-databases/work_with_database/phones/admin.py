from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'release_date', 'lte_exists', 'slug')
    list_editable = ('lte_exists',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Phone, PhoneAdmin)
