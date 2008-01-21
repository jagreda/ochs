from django.db import models
import glob, os
from PIL import Image
from tnjn.settings import IMAGE_UPLOAD_PATH, IMAGE_FILE_PATH, SIZE_THUMBNAIL, SIZE_RESIZE, SIZE_SIDEBAR, SIZE_BOX, SIZE_STORY02, SIZE_HOME04
from tnjn.settings import COUNT as RANK
from tnjn.newssite.models import *
from tnjn.staff.models import *

imagepath = IMAGE_FILE_PATH

MEDIA_TYPE = (
    ('Audio', 'AUDIO'),
    ('PDF', 'PDF'),
    ('Image', 'IMAGE'),
    ('Html', 'HTML'),
    ('Note', 'NOTES'),
    ('Error', 'ERROR'),
)

class images(models.Model):
    story = models.ForeignKey(
        Story,
        help_text = """ """,
        edit_inline = models.TABULAR,
        num_in_admin = 1,
        num_extra_on_change = 1,
        )
    description = models.CharField(
        max_length = 9000,
        help_text = """ """,
        verbose_name = "Description",
        blank = True,
        )
    source = models.CharField(
        max_length = 100,
        help_text = """ """,
        verbose_name = "Source",
        core = True,
        )
    file = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "File",
        width_field = "width",
        height_field = "height",
        core = True,
        )
    width = models.CharField(
        max_length = 10,
        help_text = """ """,
        editable = False,
        null = True,
        blank = True,
        )
    height = models.CharField(
        max_length = 10,
        help_text = """ """,
        editable = False,
        null = True,
        blank = True,
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        help_text = """ """,
        blank = True,
        editable = False,
        )
    thumbnail = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "Thumbnail",
        blank = True,
        null = True,
        editable = False,
        )
    resize = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "resize",
        blank = True,
        null = True,
        editable = False,
        )
    sidebar = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "resize",
        blank = True,
        null = True,
        editable = False,
        )
    box = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "resize",
        blank = True,
        null = True,
        editable=False,
        )
    photog_byline = models.ForeignKey(
        UserProfile,
        help_text = """ """,
        related_name = "photog2",
        verbose_name = "Photographer",
        blank = True,
        null = True,
        )
    story02 = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "resize",
        blank = True,
        null = True,
        editable = False,
        )
    home04 = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        verbose_name = "resize",
        help_text = """ """,
        blank = True,
        null = True,
        editable = False,
        )
    sort = models.CharField(
        choices = RANK,
        help_text = """ """,
        max_length = 2,
        verbose_name = "Rank",
        )

    def get_absolute_url(self):
        return "/%s" % self.file

    def get_resize_url(self):
        return "/%s" % self.resize

    def get_box_url(self):
        return "/%s" % self.box

    def get_sidebar_url(self):
        return "/%s" % self.sidebar

    def get_story02_url(self):
        return "/%s" % self.story02

    def get_home04_url(self):
        return "/%s" % self.home04

    def get_thumbnail_url(self):
        return "/%s" % self.thumbnail

    def __str__(self):
        return self.description

    def save(self):
        super(images,self).save()
        file_path = self.file
        if (file_path):
            img, ext = os.path.splitext(file_path)
            im = Image.open(imagepath + file_path)

            im.thumbnail(SIZE_THUMBNAIL, Image.ANTIALIAS)
            im.save(imagepath + img + ".thumb" + ext)
            self.thumbnail = img + ".thumb" + ext

            im.thumbnail(SIZE_RESIZE, Image.ANTIALIAS)
            im.save(imagepath + img + ".512" + ext)
            self.resize = img + ".512" + ext

            im.thumbnail(SIZE_SIDEBAR, Image.ANTIALIAS)
            im.save(imagepath + img + ".220" + ext)
            self.sidebar = img + ".220" + ext

            im.thumbnail(SIZE_BOX, Image.ANTIALIAS)
            im.save(imagepath + img + ".box" + ext)
            self.box = img + ".box" + ext

            im.thumbnail(SIZE_STORY02, Image.ANTIALIAS)
            im.save(imagepath + img + ".story02" + ext)
            self.story02 = img + ".story02" + ext

            im.thumbnail(SIZE_HOME04, Image.ANTIALIAS)
            im.save(imagepath + img + ".home04" + ext)
            self.home04 = img + ".home04" + ext
        super(images2,self).save()

    def show_thumb(self):
        file_path = self.get_absolute_url()
        file, ext = os.path.splitext(file_path)
        file = file + ".thumb" + ext
        if(file_path):
            return '<a href="%s"><img src="%s" border="0" /></a>' % (self.id,file)
    show_thumb.allow_tags = True
    show_thumb.short_description='Image'

    def columnTwo(self):
        return '<a href="/admin/newssite/images2/%s/delete/" class="deletelink">DELETE</a>' % (self.id)
    columnTwo.allow_tags = True
    columnTwo.short_description='Media Mate'

    def descript(self):
        return self.description
    descript.allow_tags = True
    descript.short_description='Caption'

    def src(self):
        return self.source
    src.allow_tags = True
    src.short_description='Source'

    def delete(self):
        file_path = self.get_absolute_url()
        if os.path.exists(file_path):
            file, ext = os.path.splitext(file_path)
            thumb = file + ".thumbnail" + ext
            resize = file + ".512" + ext
            sidebar = file + ".220" + ext
            if(thumb):
                try:
                    os.remove(imagepath + thumb)
                except:
                    pass
            if(resize):
                try:
                    os.remove(imagepath + resize)
                except:
                    pass
            if(sidebar):
                try:
                    os.remove(imagepath + sidebar)
                except:
                    pass
            if(file_path):
                try:
                    os.remove(imagepath + file_path)
                except:
                    pass
        super(images, self).delete()

    class Admin:
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
        search_fields = (
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

    class Meta:
        verbose_name = "Story Images"
        verbose_name_plural = "Story Images"
        ordering = ('sort',)

class media(models.Model):
    story = models.ForeignKey(
        Story,
        help_text = """ """,
        edit_inline = models.TABULAR,
        num_in_admin = 1,
        num_extra_on_change = 1,
        )
    media_type = models.CharField(
        core = True,
        max_length = 10,
        choices = MEDIA_TYPE,
        help_text = """Audio: When uploading MP3's <br /> \
            PDF: When uploading PDF's<br /> \
            Image: When uploading and images<br /> \
            HTML: When creating lists, custom HTML, embedding YouTube video and a \
                general scratch pad<br />\
            Note: A lot like HTML and may be rolled into HTML.<br />\
            Error: Site Admins will flag media with this label when it contains an \
                error or breaks the site.""",
        default = "Image",
        verbose_name = "Related Media Type",
        )
    description = models.TextField(
        blank = True,
        verbose_name = "Description",
        help_text = """<strong>To edit the HTML associated with this description, \
            click the HTML icon in the editor above.</strong>""",
            )
    source = models.CharField(
        max_length = 100,
        verbose_name = "Source",
        help_text = """ """,
        blank = True,
        null = True,
        editable = False,
        )
    file = models.FileField(
        upload_to = IMAGE_UPLOAD_PATH,
        verbose_name = "File",
        blank = True,
        null = True,
        help_text = """Only upload a file if the media type is:<br />\
            1)Audio - the file must be a mp3, otherwise it will not play on the site.<br />\
            2)PDF - the file must be a PDF.<br />\
            3)Image - the file should be a gif, jpg, png or other web standard image.<br />\
                Do not upload program specific files (examples: psd, ai, etc)""",
        )
    modified_date = models.DateTimeField(
        auto_now = True,
        help_text = """ """,
        blank = True,
        editable = False,
        )
    thumbnail = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "Thumbnail",
        blank = True,
        null = True,
        editable = False,
        )
    resize = models.ImageField(
        upload_to = IMAGE_UPLOAD_PATH,
        help_text = """ """,
        verbose_name = "resize",
        blank = True,
        null = True,
        editable = False,
        )
    sort = models.CharField(
        choices = RANK,
        help_text = """ """,
        max_length = 2 ,
        verbose_name = "Rank",
        )

    def get_absolute_url(self):
        return "/%s" % self.file

    def get_resize_url(self):
        return "/%s" % self.resize

    def get_thumbnail_url(self):
        return "/%s" % self.thumbnail

    def __str__(self):
        return self.description

    def save(self):
        super(media,self).save()
        if self.media_type == "Image":
            if (self.file):
                file_path = self.file
                if (file_path):
                    img, ext = os.path.splitext(file_path)
                    im = Image.open(imagepath + file_path)

                    im.thumbnail(SIZE_THUMBNAIL, Image.ANTIALIAS)
                    im.save(imagepath + img + ".thumb" + ext)
                    self.thumbnail = img + ".thumb" + ext

                    im.thumbnail(SIZE_SIDEBAR, Image.ANTIALIAS)
                    im.save(imagepath + img + ".220" + ext)
                    self.resize = img + ".220" + ext
            super(media,self).save()

    def delete(self):
        file_path = self.get_absolute_url()
        if self.media_type == "Image":
            if os.path.exists(file_path):
                file, ext = os.path.splitext(file_path)
                thumb = file + ".thumbnail" + ext
                resize = file + ".220" + ext

                if(thumb):
                    os.remove(imagepath + thumb)
                if(resize):
                    os.remove(imagepath + resize)
                if(file_path):
                    os.remove(imagepath + file_path)
        super(media, self).delete()

    def show_thumb(self):
        if self.media_type == "Image":
            file_path = self.get_absolute_url()
            file, ext = os.path.splitext(file_path)
            file = file + ".thumb" + ext
            if(file_path):
                return '<a href="%s"><img src="%s" border="0" /></a>' % (self.id,file)
    show_thumb.allow_tags = True
    show_thumb.short_description='Image'

    def columnTwo(self):
        return 'Type: %s<br /><br /><a href="https://tnjn.com/admin/newssite/media/%s/delete/" class="deletelink">DELETE</a>' % (self.media_type,self.id)
    columnTwo.allow_tags = True
    columnTwo.short_description = 'Media Mate'

    def desc(self):
        desc = self.description
        return '%s' % (desc)
    desc.allow_tags = True
    desc.short_description = 'Description'

    def src(self):
        src = self.source
        return '%s' % (src)
    src.allow_tags = True
    src.short_description = 'Source'

    class Admin:
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
        search_fields = [
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

    class Meta:
        verbose_name = "Story Sidebar Media"
        verbose_name_plural = "Story Sidebar Media"
