from modeltranslation.manager import MultilingualManager
from wagtail.wagtailcore.models import PageManager


class MultilingualPageManager(MultilingualManager, PageManager):
    """
    Fixed version of PageManager to inherit from MultilingualManager.
    Automatic modeltranslation manager patching no longer works (Django 1.10 and newer).

    While Page.objects is patched automatically, any Page models with custom managers
    should use this or do the same manually.
    """
    pass
