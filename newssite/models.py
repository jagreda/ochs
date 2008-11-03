from django.db import models
from django.contrib.comments.models import Comment, FreeComment
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec
from ochs.settings import COUNT

from ochs.courses.models import *
from ochs.staff.models import *

STORY_STATUS = (
    ('D', 'DRAFT'),
    ('R', 'READY FOR EDITING'),
    ('E', 'READY TO PUBLISH'),
    ('P', 'PUBLISHED'),
    ('S', 'STATIC'),
    ('U', 'REJECTED'),
)

class section(models.Model):
    section_name = models.CharField(
        max_length = 200,
        )
    slug = models.CharField(
        max_length = 30,
        blank = True,
        editable = False,
        )
    parent = models.ForeignKey(
        'self',
        blank = True,
        null = True,
        related_name = 'child',
        )
    description = models.TextField(
        blank = True,
        help_text = """Optional""",
        )
    email = models.CharField(
        max_length = 200,
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    class Admin:
            list_display = (
                'section_name',
                '_parents_repr',
                )

    def __str__(self):
            p_list = self._recurse_for_parents(self)
            p_list.append(self.section_name)
            return self.get_separator().join(p_list)

    def get_absolute_url(self):
            if self.parent_id:
                    return "/%s/%s/" % (self.parent.slug, self.slug)
            else:
                    return "/%s/" % (self.slug)

    def _recurse_for_parents(self, cat_obj):
            p_list = []
            if cat_obj.parent_id:
                    p = cat_obj.parent
                    p_list.append(p.section_name)
                    more = self._recurse_for_parents(p)
                    p_list.extend(more)
            if cat_obj == self and p_list:
                    p_list.reverse()
            return p_list

    def get_separator(self):
            return ' :: '

    def _parents_repr(self):
            p_list = self._recurse_for_parents(self)
            return self.get_separator().join(p_list)
    _parents_repr.short_description = "Section parents"

    def save(self):
        p_list = self._recurse_for_parents(self)
        if self.section_name in p_list:
            raise validators.ValidationError("You must not save a section in itself!")
        self.slug = slugify( self.section_name )
        super(section, self).save()

    class Meta:
        verbose_name = "Section Fronts"
        verbose_name_plural = "Section Fronts"

class Story(models.Model):
    site = models.ManyToManyField(
        Site,
        help_text = """ """,
        )
    storysource = models.CharField(
        max_length = 200,
        blank = True,
        null = True,
        verbose_name = "Other Story Sources",
        help_text = """ """,
        )
    publish_date = models.DateTimeField(
        'Publish Date',
        help_text = """ """,
            )
    headline = models.CharField(
        max_length = 100,
        help_text=""" """,
            )
    slug = models.CharField(
        max_length = 30,
        blank = True,
        editable = False,
        )
    summary = models.TextField(
        help_text = """ """,
        verbose_name = "Summary",
        )
    body = models.TextField(
        help_text = """ """,
        verbose_name = "Body",
        )
    storysection = models.ForeignKey(
        'section',
        verbose_name = "Section",
        default = '1',
        help_text = """ """,
        )
    enable_comments = models.BooleanField(
        default = True,
        )
    breaking_news = models.BooleanField(
        help_text=""" """,
        )
    photog_review = models.BooleanField(
        verbose_name="Photographer Review Completed",
        help_text=""" """,
        )
    story_status = models.CharField(
        max_length = 1,
        choices = STORY_STATUS,
        help_text = """ """,
        default = "D",
        verbose_name = "Story Status",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )
    template = models.ForeignKey(
        'templates',
        limit_choices_to = {'status__exact' : 'A', 'type__exact' : 'A'},
        help_text = """ """,
        default = '8',
        )

    def save(self):
        self.slug = slugify( self.headline )
        super(Story,self).save()
        #ping_google()

    def get_absolute_url(self):
        return "/%s/%s/" % (self.publish_date.strftime("%Y/%b/%d").lower(), self.slug)

    def __str__(self):
        return "%s : %s" % (self.headline, self.publish_date)

    class Admin:
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

    class Meta:
        ordering = ('-publish_date',)
        verbose_name = "Story"
        verbose_name_plural = "Stories"

class medialinks(models.Model):
    story = models.ForeignKey(
        Story,
        edit_inline = models.TABULAR,
        num_in_admin = 3,
        num_extra_on_change = 3,
        )
    title = models.CharField(
        max_length = 50,
        core = True,
        verbose_name = "Link Text",
        )
    link = models.CharField(
        max_length = 300,
        core = True,
        verbose_name = "URL : Include the http:// prefix",
        help_text = """<strong>Include the <em>http://</em> prefix</strong>""",
        )
    description = models.CharField(
        max_length = 500,
        verbose_name = "Description",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    def __str__(self):
        return '%s : %s' % (self.modified_date.strftime('%m-%d-%y'), self.title)

    def save(self):
        super(medialinks,self).save()

    class Meta:
        verbose_name = "Related Link for this story"
        verbose_name_plural = "Related Links for this story"

class storybyline(models.Model):
    story = models.ForeignKey(
        Story,
        edit_inline = models.TABULAR,
        num_in_admin = 1,
        num_extra_on_change = 1,
        )
    position = models.ForeignKey(
        UserPosition,
        core = True,
        )
    byline = models.ForeignKey(
        UserProfile,
        core = True,
        )
    course = models.ForeignKey(
        course_information,
        blank = True,
        null = True,
        )

    class Admin:
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

    class Meta:
        verbose_name = "Story Finder"
        verbose_name_plural = "Story Finder"

    def st_head(self):
        return "<a href='/admin/newssite/story/%s/'>%s</a>" % (self.story.id, self.story.headline)
    st_head.admin_order_field = 'story'
    st_head.short_description = 'Headline'
    st_head.allow_tags = True

    def st_section(self):
        return self.story.storysection
    st_section.short_description = 'Section'

    def st_status(self):
        if self.story.story_status == 'Z':
            return "Story in progress"
        if self.story.story_status == 'X':
            return "Story completed"
        if self.story.story_status == 'D':
            return "Draft"
        if self.story.story_status == 'E':
            return "Ready for publishing"
        if self.story.story_status == 'R':
            return "Ready for editing"
        if self.story.story_status == 'P':
            return "Published"
        if self.story.story_status == 'S':
            return "Static"
        if self.story.story_status == 'U':
            return "Rejected"
    st_status.short_description = 'Story Status'

    def st_lastupdate(self):
        return self.story.modified_date
    st_lastupdate.short_description = 'Last Update'

    def st_publish(self):
        return self.story.publish_date
    st_publish.short_description = 'Publish Date'


class hitcount(models.Model):
    storyhit = models.ForeignKey(
        Story,
        related_name = "story_hit_count",
        )
    type = models.CharField(
        max_length = 10,
        )
    date = models.DateTimeField(
        auto_now = True,
        )

TEMPLATE_STATUS = (
    ('D', 'DEVELOPMENT'),
    ('A', 'ACTIVE'),
    ('I', 'INACTIVE'),
)

TEMPLATE_TYPE = (
    ('H', 'HOME'),
    ('S', 'SECTION'),
    ('A', 'STORY'),
)

class templates(models.Model):
    type = models.CharField(
        max_length = 1,
        choices = TEMPLATE_TYPE,
        help_text = "",
        default = "D",
        verbose_name = "Type",
        )
    status = models.CharField(
        max_length = 1,
        choices = TEMPLATE_STATUS,
        help_text = "",
        default = "H",
        verbose_name = "Status",
        )
    description = models.TextField(
        help_text = "",
        verbose_name = "Description",
        )
    system_indicator = models.CharField(
        max_length = 20,
        help_text = "",
        verbose_name = "System Indicator",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    def save(self):
        super(templates,self).save()

    def __str__(self):
        return self.system_indicator

    class Admin:
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

    class Meta:
        ordering = ('type',)
        verbose_name = "Page Templates - Add New"
        verbose_name_plural = "Page Templates - Add New "

LAYOUT_STATUS = (
    ('D', 'DRAFT'),
    ('A', 'ACTIVE'),
    ('I', 'INACTIVE'),
)

class homepage_templates(models.Model):
    site = models.ForeignKey(
        Site,
        help_text = """ """,
        )
    status = models.CharField(
        max_length = 1,
        choices = LAYOUT_STATUS,
        help_text = """DRAFT: Save page as draft when you are building it.  \
            Draft pages can be previewed using 'view on site'.<br />\
            ACTIVE: No longer draft and is puglished to the site.<br />\
            INACTIVE: Was onced published, but needed to be removed or page \
                needed to be rolled back to previous page.""", \
        default = "D",
        verbose_name = "Status",
        )
    active_date = models.DateTimeField(
        verbose_name = 'Publish Date',
        )
    template = models.ForeignKey(
        templates,
        limit_choices_to = {'status__exact' : 'A', 'type__exact' : 'H'},
        help_text = """ """,
        )
    notes = models.TextField(
        help_text = """ """,
        verbose_name = "Staff Notes"
        )
    slot1 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        related_name = "home_slot1",
        blank = True,
        null = True,
        help_text=""" """,
        )
    slot2 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot2",
        blank=True,
        null=True,
        )
    slot3 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot3",
        blank = True,
        null = True,
        )
    slot4 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot4",
        blank = True,
        null = True,
        )
    slot5 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot5",
        blank = True,
        null = True,
        )
    slot6 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot6",
        blank = True,
        null = True,
        )
    slot7 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot7",
        blank = True,
        null = True,
        )
    slot8 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot8",
        blank = True,
        null = True,
        )
    slot9 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot9",
        blank = True,
        null = True,
        )
    slot10 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "home_slot10",
        blank = True,
        null = True,
        )
    recentheadlines = models.IntegerField(
        choices = COUNT,
        help_text = "Select the number of recent headlines to display",
        default = 10,
        verbose_name = "Recent Headlines",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    def save(self):
        super(homepage_templates,self).save()

    def __str__(self):
        return self.notes

    def get_absolute_url(self):
        return "/archives/homepage/%s/%s/" % (self.active_date.strftime("%Y/%b/%d").lower(), self.id)

    class Admin:
        list_display = (
            'site',
            'active_date',
            'template',
            'modified_date',
            )

    class Meta:
        ordering = ('-active_date',)
        verbose_name = "Page Layouts - Home"
        verbose_name_plural = "Page Layouts - Home"

class section_templates(models.Model):
    site = models.ForeignKey(
        Site,
        help_text = """ """,
        )
    status = models.CharField(
        max_length = 1,
        choices = LAYOUT_STATUS,
        help_text = "",
        default = "D",
        verbose_name = "Status",
        )
    storysection = models.ForeignKey(
        section,
        verbose_name = "Section(s)",
        default = '1',
        )
    active_date = models.DateTimeField(
        verbose_name = 'Publish Date',
        )
    template = models.ForeignKey(
        templates,
        limit_choices_to = {'status__exact' : 'A', 'type__exact' : 'S'},
        help_text = "",
        )
    notes = models.TextField(
        help_text="",
        verbose_name="Staff Notes",
        )
    slot1 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot1",
        blank = True,
        null = True,
        )
    slot2 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot2",
        blank = True,
        null = True,
        )
    slot3 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot3",
        blank = True,
        null = True,
        )
    slot4 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot4",
        blank = True,
        null = True,
        )
    slot5 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot5",
        blank = True,
        null = True,
        )
    slot6 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot6",
        blank = True,
        null = True,
        )
    slot7 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot7",
        blank = True,
        null = True,
        )
    slot8 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot8",
        blank = True,
        null = True,
        )
    slot9 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot9",
        blank = True,
        null = True,
        )
    slot10 = models.ForeignKey(
        Story,
        limit_choices_to = {'story_status__iexact' : 'P'},
        help_text = "",
        related_name = "section_slot10",
        blank = True,
        null = True,
        )
    recentheadlines = models.IntegerField(
        choices = COUNT,
        help_text = "Select the number of recent headlines to display",
        default = 10,
        verbose_name = "Recent Headlines",
        )
    photostream = models.IntegerField(
        choices = COUNT,
        help_text = "Select the number of photo stream objects to display",
        default = 5,
        verbose_name = "Photo Stream",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    def save(self):
        super(section_templates,self).save()

    def get_absolute_url(self):
        return "/archives/section/%s/%s/%s/" % (self.storysection.slug, self.active_date.strftime("%Y/%b/%d").lower(), self.id)

    def __str__(self):
        return self.notes

    class Admin:
        list_display = (
            'site',
            'active_date',
            'storysection',
            'template',
            'modified_date',
            )

    class Meta:
        ordering = ('-active_date',)
        verbose_name = "Page Layouts - Sections"
        verbose_name_plural = "Page Layouts - Sections"


