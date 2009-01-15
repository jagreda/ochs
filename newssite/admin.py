from django.contrib import admin
from models import section

class sectionAdmin (admin.ModelAdmin):
    list_display = (
        'section_name',
        '_parents_repr',
        )

admin.site.register(section, sectionAdmin)

class storybylineInline(admin.TabularInline):
    model = storybyline
    extra = 1

class medialinksInline(admin.TabularInline):
    model = medialinks
    extra = 3

class.storyAdmin (admin.ModelAdmin):
    js = ['tiny_mce/tiny_mce.js', 'js/textareas.js']
    fields = (
        (None, {
            'fields' : ('site', 'publish_date', 'story_status', 'photog_review', 'enable_comments', 'breaking_news', 'template', 'headline', 'summary', 'body', 'storysection', 'storysource',)
        }),
    )
    list_display = (
        'headline',
        'storysection',
        'story_status',
        'publish_date',
        'modified_date',
        )
    list_filter = [
        'site',
        'photog_review',
        'story_status',
        'publish_date',
        'storysection',
        ]
    search_fields = [
        'headline',
        'summary',
        'body',
        ]
    date_hierarchy = 'publish_date'
    list_per_page = 25
    inlines = [
        medialinksInline,
        storybylineInline,
    ]

admin.site.register(story, storyAdmin)

class.storybylineAdmin (admin.ModelAdmin):
    list_display = (
        'st_head',
        'position',
        'byline',
        'course',
        'st_section',
        'st_status',
        'st_lastupdate',
        'st_publish',
        )
    list_filter = [
        'position',
        'course',
        ]
    search_fields = [
        'story__headline',
        'byline__first_name',
        'byline__last_name',
        ]

admin.site.register(storybyline, storybylineAdmin)

class.templatesAdmin (admin.ModelAdmin):
    list_display = (
        'system_indicator',
        'type',
        'status',
        'description',
        'modified_date',
        )
    list_filter = [
        'type',
        'status',
        ]
    search_fields = [
        'type',
        'status',
        'description',
        'system_indicator',
        'modified_date',
        ]
    date_hierarchy = 'modified_date'

admin.site.register(templates, templatesAdmin)

class.homepage_templatesAdmin (admin.ModelAdmin):
    list_display = (
        'site',
        'active_date',
        'template',
        'modified_date',
        )

admin.site.register(homepage_templates, homepage_templatesAdmin)

class.section_templatesAdmin (admin.ModelAdmin):
    list_display = (
        'site',
        'active_date',
        'storysection',
        'template',
        'modified_date',
        )

admin.site.register(section_templates, section_templatesAdmin)