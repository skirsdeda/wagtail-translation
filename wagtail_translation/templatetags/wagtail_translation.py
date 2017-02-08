from __future__ import unicode_literals

from django import template
from django.utils.translation import get_language_from_path, override
from django.utils.translation.trans_real import language_code_prefix_re
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR, AbstractPage

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang(context, lang_code):
    if 'request' in context:
        request = context['request']

        if PAGE_TEMPLATE_VAR in context and isinstance(context[PAGE_TEMPLATE_VAR], AbstractPage):
            # current request points to a Wagtail page
            page = context[PAGE_TEMPLATE_VAR]

            with override(lang_code):
                trans_url_path = page.url_path
                non_trans_page = trans_url_path.find('//')
                if non_trans_page > 0:
                    trans_url_path = trans_url_path[:non_trans_page]
                    path_components = [comp for comp in trans_url_path.split('/')]
                    page, args, kwargs = request.site.root_page.specific.route(request, path_components)
                elif non_trans_page == 0:
                    # root page not translated!
                    return ''
                return page.url
        elif 'object' in context:
            # for cases when DetailView or similar is used
            obj = context['object']
            with override(lang_code):
                try:
                    return obj.get_absolute_url()
                except:
                    pass

        # if none of the above URL translation methods worked
        # let's try replacing language prefix in URL
        current_lang = get_language_from_path(request.path_info)
        if current_lang is not None:
            return language_code_prefix_re.sub('/{}/'.format(lang_code), request.path_info)

    return ''
