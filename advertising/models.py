from django.db import models
from tnjn.newssite.models import section

O_TYPE = (
    ('A', 'SLOT 1'),
    ('B', 'SLOT 2'),
    ('C', 'SLOT 3'),
    ('D', 'SLOT 4'),
    ('E', 'SLOT 5'),
    ('F', 'SLOT 6'),
    ('G', 'SLOT 7'),
    ('H', 'SLOT 8'),
    ('I', 'SIDEBAR'),
)

O_AREA = (
    ('A', 'HOME PAGE'),
    ('B', 'SECTION PAGE'),
    ('C', 'STORY PAGE'),
)


ADS_STATUS = (
    ('A', 'DRAFT'),
    ('B', 'PUBLISHED'),
)

class ads(models.Model):
    customer = models.CharField(
        max_length = 200,
        )
    start_date = models.DateField(
        'Start Date',
        help_text = "Enter the start date of the ad.",
        )
    end_date = models.DateField(
        'End Date',
        help_text = "Enter the end date of the ad.",
        )
    area = models.CharField(
        max_length = 1,
        choices = O_AREA,
        help_text = "",
        verbose_name = "Ad Area",
        )
    section = models.ForeignKey(
        section,
        blank=True,
        null=True,
        help_text="If this is a section page ad, please indiate what section it belongs to",
        )
    type = models.CharField(
        max_length = 1,
        choices = O_TYPE,
        help_text = "",
        verbose_name = "Ad Slot",
        )
    status = models.CharField(
        max_length = 1,
        choices = ADS_STATUS,
        help_text = "Current Status of this ad.",
        verbose_name = "Ad Status",
        )
    file = models.ImageField(
        upload_to = "content/advertising/online/%Y/%m/%d",
        verbose_name = "Ad File",
        )
    link = models.URLField(
        blank = True,
        null = True,
        help_text = "",
        )
    salesrep = models.CharField(
        max_length = 50,
        blank = True,
        editable = False,
        )

    class Admin:
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
    class Meta:
        ordering = ('-end_date',)
        verbose_name = "Ads"
        verbose_name_plural = "Ads"