from staff.models import UserPosition, UserProfile
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class UserPositionOptions(admin.ModelAdmin):
    list_display = (
        'position',
        )
    search_fieldsets = [
        'position',
        ]
    ordering = [
        'position',
        ]

class UserProfileOptions(admin.ModelAdmin):
    list_display = (
        'username',
        'last_name',
        'first_name',
        'email',
        'active',
        'created_date',
        'modified_date',
        )
    search_fieldsets = [
        'username__username',
        'first_name',
        'last_name',
        'modified_date',
        ]
    date_hierarchy = 'modified_date'
    ordering = [
        'last_name',
        'first_name',
        ]

admin.site.register(UserPosition, UserPositionOptions)
admin.site.register(UserProfile, UserProfileOptions)

