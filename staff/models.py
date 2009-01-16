from django.db import models
from django.contrib.auth.models import User

class UserPosition(models.Model):
    position = models.CharField(
        max_length = 50,
        help_text = """ """,
        unique = True,
        )

    class Admin:
        list_display = (
            'position',
            )
        search_fields = [
            'position',
            ]
        ordering = [
            'position',
            ]

    class Meta:
        ordering = (
            'position',
            )

class UserProfile(models.Model):
    username = models.OneToOneField(
        User,
        related_name = "staff_user",
        help_text = """ """,
        )
    hometown = models.CharField(
        max_length = 50,
        help_text = """ """,
        blank = True,
        )
    photo = models.ImageField(
        upload_to = "content/staff",
        verbose_name = "File",
        help_text = """ """,
        blank = True,
        )
    bio = models.TextField(
        blank = True,
        help_text = """ """,
        )
    last_name = models.CharField(
        max_length = 200,
        help_text = """ """,
        editable = False,
        blank = True,
        )
    first_name =  models.CharField(
        max_length = 200,
        help_text = """ """,
        editable = False,
        blank = True,
        )
    email = models.CharField(
        max_length = 200,
        editable = False,
        help_text = """ """,
        blank = True,
        )
    created_date = models.DateTimeField(
        blank = True,
        editable = False,
        help_text = """ """,
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        help_text = """ """,
        )

    def save(self):
        if self.username:
            self.last_name = self.username.last_name
            self.first_name = self.username.first_name
            self.email = self.username.email
            self.created_date = self.username.date_joined
            super(UserProfile,self).save()

    def get_absolute_url(self):
        return "/staff/%s/" % (self.user)

    def get_list(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def active(self):
        if self.user.is_active:
            status = "Active User"
        else:
            status = "Inactive User"
        return '%s' % (status)
    active.short_description='Status'

    def realname(self):
        return '%s, %s' % (self.last_name, self.first_name)
    realname.short_description='Name'

    class Admin:
        list_display = (
            'username',
            'last_name',
            'first_name',
            'email',
            'active',
            'created_date',
            'modified_date',
            )
        search_fields = [
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

    class Meta:
        ordering = (
            'last_name',
            'first_name',
            )