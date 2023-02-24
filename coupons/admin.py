from django.contrib import admin
from .models import Page, Website


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['site', 'name', 'url', 'coupon']

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
