from django.contrib import admin
from .models import Page, Website, Logs


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'coupon']

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ['msg']
