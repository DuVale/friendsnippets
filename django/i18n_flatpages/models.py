from django.core import validators
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
        help_text=_("Example: '/about/contact/'. Make sure to have leading and trailing slashes."))
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)
    class Meta:
        db_table = 'django_flatpage'
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)
    class Admin:
        fields = (
            (None, {'fields': ('url', 'title', 'content', 'sites')}),
            ('Advanced options', {'classes': 'collapse', 'fields': ('enable_comments', 'registration_required', 'template_name')}),
        )
        list_filter = ('sites',)
        search_fields = ('url', 'title')

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class TranslatedFlatPage(models.Model):
    page = models.ForeignKey(FlatPage, edit_inline=models.TABULAR)
    lang = models.CharField(max_length=10)
    title = models.CharField(_('title'), max_length=200, core=True)
    content = models.TextField(_('content'), core=True)

    def __unicode__(self):
        return u"%s - %s" % (self.page, self.lang)

    class Admin:
        list_filter = ('lang',)
        search_fields = ('page',)



