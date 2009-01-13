from django.contrib import admin
from models import section

class sectionAdmin (admin.ModelAdmin):
    list_display = (
        'section_name',
        '_parents_repr',
        )

admin.site.register(section, sectionAdmin)