from importlib import import_module
from django.apps import AppConfig


class WagtailTranslationAppConfig(AppConfig):
    name = 'wagtail_translation'
    label = 'wagtailtranslation'
    verbose_name = 'Wagtail translation'

    def ready(self):
        # patch Site and Page models here
        from wagtail.wagtailcore.models import Page, Site
        from wagtail.wagtailcore.query import PageQuerySet

        page_patch = import_module('wagtail_translation.page_patch')
        site_patch = import_module('wagtail_translation.site_patch')
        query_patch = import_module('wagtail_translation.query_patch')

        for name in page_patch.__all__:
            setattr(Page, name, getattr(page_patch, name))
        for name in site_patch.__all__:
            setattr(Site, name, getattr(site_patch, name))
        for name in query_patch.__all__:
            setattr(PageQuerySet, name, getattr(query_patch, name))
