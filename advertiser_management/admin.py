from django.contrib import admin
from .models import Advertiser
from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertiser']
    readonly_fields = ('title', 'link', 'image', 'advertiser')
    list_filter = ['approve']
    search_fields = ['title']

admin.site.register(Advertiser)
