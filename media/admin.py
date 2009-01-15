from media.models import images, media
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class images_Inline(admin.TabularInline):
    model = images
    extra = 1

class media_Inline(admin.TabularInline):
    model = media
    extra = 1

class imagesOptions(admin.ModelAdmin):
    list_filter = [
        'modified_date',
    ]
    list_display = (
        'columnTwo',
        'show_thumb',
        'descript',
        'photog_byline',
        'src',
        'modified_date',
    )
    search_fieldsets = (
        'description',
        'source',
        'photog_byline_id',
        'modified_date',
        )
    date_hierarchy = 'modified_date'
    ordering = [
        '-modified_date',
        'media_type',
        ]
    list_per_page = 25

class mediaOptions(admin.ModelAdmin):
    list_filter = [
        'media_type',
        'modified_date',
        ]
    list_display = (
        'columnTwo',
        'show_thumb',
        'desc',
        'modified_date',
        )
    search_fieldsets = [
        'media_type',
        'description',
        'source',
        'modified_date',
        ]
    date_hierarchy = 'modified_date'
    ordering = [
        '-modified_date',
        'media_type',
        ]
    list_per_page = 25

# class StoryOptions(admin.ModelAdmin):
#     inlines = [images_Inline, media_Inline]

admin.site.register(images, imagesOptions)
admin.site.register(media, mediaOptions)

