from __future__ import absolute_import, unicode_literals

import warnings

from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname


def get_lang_obj(lang_code, cls, field_name, *args, **kwargs):
    """
    Instantiates any `cls` with localized fieldname as the first
    argument to it's constructor.
    """
    return cls(build_localized_fieldname(field_name, lang_code), *args, **kwargs)


def obj_per_lang(cls, field_name, *args, **kwargs):
    """
    Returns an array of instantiated `cls` using localized fieldname
    for each language as the first argument to it's constructor.
    """
    langs = kwargs.pop('languages', mt_settings.AVAILABLE_LANGUAGES)
    ret = []
    # make sure default lang always goes first
    if mt_settings.DEFAULT_LANGUAGE in langs:
        obj = get_lang_obj(
            mt_settings.DEFAULT_LANGUAGE,
            cls,
            field_name,
            *args, **kwargs
        )
        ret.append(obj)

    for lang_code in langs:
        if lang_code != mt_settings.DEFAULT_LANGUAGE:
            obj = get_lang_obj(
                lang_code,
                cls,
                field_name,
                *args, **kwargs
            )
            ret.append(obj)
    return ret


def page_slug_is_available(slug, lang_code, parent_page, page=None):
    """
    Determines whether a slug is available for a page in
    a specified language.
    """
    if parent_page is None:
        return True

    siblings = parent_page.get_children()
    if page:
        siblings = siblings.not_page(page)

    slug_f = build_localized_fieldname('slug', lang_code)
    return not siblings.filter(**{slug_f: slug}).exists()


def deprecated(obj):
    if isinstance(obj, type):
        return _deprecated_cls(cls=obj)
    else:
        return _deprecated_func(f=obj)


def _deprecated_func(f, warn_cls=DeprecationWarning):
    def _deprecated(*args, **kwargs):
        message = "Method '%s' is deprecated and will be " \
            "removed in the next version of wagtail-translation" \
            % f.__name__
        warnings.warn(message, warn_cls, stacklevel=2)
        return f(*args, **kwargs)
    return _deprecated


def _deprecated_cls(cls, warn_cls=DeprecationWarning):
    class Deprecated(cls):
        def __init__(self, *args, **kwargs):
            message = "Class '%s' is deprecated and will be " \
                "removed in the next version of wagtail-translation" \
                % cls.__name__
            warnings.warn(message, warn_cls, stacklevel=2)
            super(Deprecated, self).__init__(*args, **kwargs)
    return Deprecated
