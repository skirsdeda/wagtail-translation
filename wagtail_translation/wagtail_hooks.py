import json

from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def translated_slugs():
    js_files = [
        'wagtail_translation/js/wagtail_translated_slugs.js',
    ]

    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>', (
        (settings.STATIC_URL, filename) for filename in js_files)
    )

    lang_codes = [lang_code for lang_code, l in settings.LANGUAGES]
    js_languages = '<script>var langs={};</script>'.format(json.dumps(lang_codes))

    return format_html(js_languages) + js_includes
