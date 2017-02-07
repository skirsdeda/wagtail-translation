from importlib import import_module
from django.apps import AppConfig


class WagtailTranslationAppConfig(AppConfig):
    name = 'wagtail_translation'
    label = 'wagtailtranslation'
    verbose_name = 'Wagtail translation'

    def ready(self):
        # patch Page model here
        from wagtail.wagtailcore.models import Page
        page_patch = import_module('wagtail_translation.page_patch')

        for name in page_patch.__all__:
            setattr(Page, name, getattr(page_patch, name))
