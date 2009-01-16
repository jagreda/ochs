from django.db import models
from ochs.staff.models import UserProfile

TERM_LIST= (
    ('SPRING', 'SPRING'),
    ('MINI', 'MINI'),
    ('SUMMER', 'SUMMER'),
    ('FALL', 'FALL'),
    )

class course_information(models.Model):
    course = models.CharField(
        max_length = 10,
        )
    title =  models.CharField(
        max_length = 1000,
        )
    section = models.CharField(
        max_length = 3,
        )
    term = models.CharField(
        choices = TERM_LIST,
        max_length = 10,
        )
    year = models.CharField(
        max_length = 4,
        help_text = "Four Character Year (eg: 2006)",
        )
    professor = models.ForeignKey(
        UserProfile,
        related_name = "professor",
        limit_choices_to = {'username__groups__name__iexact' : 'Faculty'},
        verbose_name = "Professor",
        )
    description = models.TextField()
    modified_date = models.DateTimeField(
        auto_now = True,
        blank = True,
        editable = False,
        )

    def save(self):
        super(course_information,self).save()

    def get_absolute_url(self):
        return "/course/%s/" % self.id

    def __unicode__(self):
        return '%s %s : %s : %s' % (self.term, self.year, self.course, self.section)

    def quick(self):
        return '%s %s : %s : %s' % (self.term, self.year, self.course, self.section)

    class Admin:
        list_display = (
            'course',
            'section',
            'term',
            'year',
            'title',
            'professor',
            'modified_date',
            )
        search_fields = [
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

    class Meta:
        verbose_name = "Course Information"
        verbose_name_plural = "Course Information"
        ordering = (
            '-year',
            'term',
            'course',
            'section',
            )