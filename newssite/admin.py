from newssite.models import section, Story, medialinks, storybyline, templates, homepage_templates, section_templates
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class medialinks_Inline(admin.TabularInline):
    model = medialinks
    extra = 3

class storybyline_Inline(admin.TabularInline):
    model = storybyline
    extra = 1

class templatesOptions(admin.ModelAdmin):
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
    search_fieldsets = [
        'type',
        'status',
        'description',
        'system_indicator',
        'modified_date',
        ]
    date_hierarchy = 'modified_date'

class section_templatesOptions(admin.ModelAdmin):
    list_display = (
        'site',
        'active_date',
        'storysection',
        'template',
        'modified_date',
        )

class StoryOptions(admin.ModelAdmin):
    inlines = [medialinks_Inline, storybyline_Inline]
    js = ['tiny_mce/tiny_mce.js', 'js/textareas.js']
    fieldsets = (
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
    search_fieldsets = [
        'headline',
        'summary',
        'body',
        ]
    date_hierarchy = 'publish_date'
    list_per_page = 25

class storybylineOptions(admin.ModelAdmin):
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
    search_fieldsets = [
        'story__headline',
        'byline__first_name',
        'byline__last_name',
        ]

class sectionOptions(admin.ModelAdmin):
        list_display = (
            'section_name',
            '_parents_repr',
            )

class homepage_templatesOptions(admin.ModelAdmin):
    list_display = (
        'site',
        'active_date',
        'template',
        'modified_date',
        )

admin.site.register(templates, templatesOptions)
admin.site.register(section_templates, section_templatesOptions)
admin.site.register(Story, StoryOptions)
admin.site.register(storybyline, storybylineOptions)
admin.site.register(section, sectionOptions)
admin.site.register(homepage_templates, homepage_templatesOptions)

