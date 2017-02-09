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
                # find position of first non-translated page in path (if any)
                non_trans_page = trans_url_path.find('//')
                if non_trans_page > 0:
                    # non-translated page found in path
                    root_page = request.site.root_page.specific
                    # get part of path from root path to first non-translated page
                    trans_url_path = trans_url_path[len(root_page.url_path):non_trans_page]
                    path_components = [comp for comp in trans_url_path.split('/') if comp]
                    # try to get that page
                    try:
                        page, args, kwargs = root_page.route(request, path_components)
                    except:
                        return ''
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
