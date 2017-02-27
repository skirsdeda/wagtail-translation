from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel

from .utils import deprecated, get_lang_obj, obj_per_lang


@deprecated
def get_lang_panel(lang_code, panel_cls, field_name, *args, **kwargs):
    return get_lang_obj(lang_code, panel_cls, field_name, *args, **kwargs)


@deprecated
def multiply_panels_per_lang(panel_cls, field_name, *args, **kwargs):
    return obj_per_lang(panel_cls, field_name, *args, **kwargs)


# replacements for Page.content_panels and Page.promote_panels to include translated fields
content_panels = obj_per_lang(FieldPanel, 'title', classname='full title')
promote_panels = [
    MultiFieldPanel(
        obj_per_lang(FieldPanel, 'slug') +
        obj_per_lang(FieldPanel, 'seo_title') +
        [FieldPanel('show_in_menus')] +
        obj_per_lang(FieldPanel, 'search_description'),
        _('Common page configuration')
    )
]
