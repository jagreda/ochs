from courses.models import course_information
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class course_informationOptions(admin.ModelAdmin):
    list_display = (
        'course',
        'section',
        'term',
        'year',
        'title',
        'professor',
        'modified_date',
        )
    search_fieldsets = [
        'course',
        'section',
        'professor',
        'term',
        'year',
        'modified_date',
        ]
    ordering = [
        '-year',
        'term',
        'course',
        'section',
        ]

admin.site.register(course_information, course_informationOptions)

