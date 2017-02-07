from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from django.utils.translation import ugettext_lazy as _


def multiply_panels_per_lang(panel_cls, field_name, *args, **kwargs):
    def get_lang_panel(lang_code):
        return panel_cls(build_localized_fieldname(field_name, lang_code), *args, **kwargs)

    panels = [
        get_lang_panel(mt_settings.DEFAULT_LANGUAGE), #  make sure default lang always goes first
    ]
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        if lang_code != mt_settings.DEFAULT_LANGUAGE:
            panels.append(get_lang_panel(lang_code))
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
