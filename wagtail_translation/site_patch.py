from __future__ import absolute_import, unicode_literals

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.utils.translation import get_language
from modeltranslation import settings as mt_settings
from wagtail.wagtailcore.models import Site

__all__ = ['get_site_root_paths']


ROOT_PATHS_CACHE_KEY_FMT = 'wagtail_site_root_paths_{}'


@staticmethod
def get_site_root_paths():
    lang = get_language()
    cache_key = ROOT_PATHS_CACHE_KEY_FMT.format(lang)

    result = cache.get(cache_key)

    if result is None:
        result = [
            (site.id, site.root_page.url_path, site.root_url)
            for site in Site.objects.select_related('root_page').order_by('-root_page__url_path')
        ]
        cache.set(cache_key, result, 3600)

    return result


def delete_root_path_cache(sender, instance, **kwargs):
    for lang in mt_settings.AVAILABLE_LANGUAGES:
        cache.delete(ROOT_PATHS_CACHE_KEY_FMT.format(lang))

post_save.connect(delete_root_path_cache, sender=Site)
post_delete.connect(delete_root_path_cache, sender=Site)
