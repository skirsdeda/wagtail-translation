from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from django.utils.translation import ugettext_lazy as _


def get_lang_panel(lang_code, panel_cls, field_name, *args, **kwargs):
    return panel_cls(build_localized_fieldname(field_name, lang_code), *args, **kwargs)


def multiply_panels_per_lang(panel_cls, field_name, *args, **kwargs):
    langs = kwargs.pop('languages', mt_settings.AVAILABLE_LANGUAGES)
    panels = []
    # make sure default lang always goes first
    if mt_settings.DEFAULT_LANGUAGE in langs:
        panel = get_lang_panel(
            mt_settings.DEFAULT_LANGUAGE,
            panel_cls,
            field_name,
            *args, **kwargs
        )
        panels.append(panel)

    for lang_code in langs:
        if lang_code != mt_settings.DEFAULT_LANGUAGE:
            panel = get_lang_panel(
                lang_code,
                panel_cls,
                field_name,
                *args, **kwargs
            )
            panels.append(panel)
    return panels


# replacements for Page.content_panels and Page.promote_panels to include translated fields
content_panels = multiply_panels_per_lang(FieldPanel, 'title', classname='full title')
promote_panels = [
    MultiFieldPanel(
        multiply_panels_per_lang(FieldPanel, 'slug') +
        multiply_panels_per_lang(FieldPanel, 'seo_title') +
        [FieldPanel('show_in_menus')] +
        multiply_panels_per_lang(FieldPanel, 'search_description'),
        _('Common page configuration')
    )
]
