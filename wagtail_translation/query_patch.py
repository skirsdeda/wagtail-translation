from __future__ import absolute_import, unicode_literals

from django.utils.translation import get_language
from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname
from wagtail.wagtailsearch.queryset import SearchableQuerySetMixin

__all__ = ['search']


def search(self, *args, **kwargs):
    if 'fields' in kwargs and 'title' in kwargs['fields']:
        # when fields are set and 'title' is one of them
        # replace it with localized field
        fields = list(kwargs['fields'])
        lang_code = get_language()  # default to current language
        # fallback to default language if current language not in translated ones
        if lang_code not in mt_settings.AVAILABLE_LANGUAGES:
            lang_code = mt_settings.DEFAULT_LANGUAGE
        fields[fields.index('title')] = build_localized_fieldname('title', lang_code)
        kwargs['fields'] = fields
    return SearchableQuerySetMixin.search(self, *args, **kwargs)

