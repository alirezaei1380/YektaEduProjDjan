from django.contrib import admin
from .models import Advertiser
from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'link', 'image', 'advertiser')


admin.site.register(Advertiser)
