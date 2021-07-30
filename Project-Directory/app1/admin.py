from django.contrib import admin
from .models import SiteWide

@admin.register(SiteWide)
class SiteSettings(admin.ModelAdmin):
    list_display = ['sitename']
