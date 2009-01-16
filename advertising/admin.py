from advertising.models import ads
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class adsOptions(admin.ModelAdmin):
    list_display = (
        'customer',
        'type',
        'section',
        'status',
        'start_date',
        'end_date',
        )
    date_hierarchy = 'end_date'
    list_filter = [
        'type',
        'section',
        'status',
        'end_date',
        'start_date',
        ]
    ordering = [
        'end_date',
        ]

admin.site.register(ads, adsOptions)

