from importlib import import_module

from django.apps import AppConfig


class WagtailTranslationAppConfig(AppConfig):
    name = 'wagtail_translation'
    label = 'wagtailtranslation'
    verbose_name = 'Wagtail translation'

    def ready(self):
        # patch Site and Page models here
        from wagtail.wagtailcore.models import AbstractPage, Page, Site
        from wagtail.wagtailcore.query import PageQuerySet
        from .manager import MultilingualPageManager

        # fix PageManager to inherit from MultilingualManager
        # since automatic manager patching no longer works (Django 1.10 and newer)
        AbstractPage.objects = MultilingualPageManager()
        AbstractPage.objects.contribute_to_class(AbstractPage, 'objects')
        Page.objects = MultilingualPageManager()
        Page.objects.contribute_to_class(Page, 'objects')

        page_patch = import_module('wagtail_translation.page_patch')
        site_patch = import_module('wagtail_translation.site_patch')
        query_patch = import_module('wagtail_translation.query_patch')

        for name in page_patch.__all__:
            setattr(Page, name, getattr(page_patch, name))
        for name in site_patch.__all__:
            setattr(Site, name, getattr(site_patch, name))
        for name in query_patch.__all__:
            setattr(PageQuerySet, name, getattr(query_patch, name))
