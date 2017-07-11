# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from modeltranslation import settings as mt_settings
from modeltranslation.utils import build_localized_fieldname, get_translation_fields
from django.db import migrations, models


def url_path_fix(apps, schema_editor):
    # cannot use apps.get_model here
    # because Page instances wouldn't have set_url_path method
    from wagtail.wagtailcore.models import Page

    url_path_fields = get_translation_fields('url_path')
    for page in Page.objects.order_by('path').iterator():
        page.set_url_path(page.get_parent())
        # make sure descendant page url paths are not updated at this point
        # because it would fail
        page.save(update_fields=url_path_fields)


class Migration(migrations.Migration):
    """
    This migration fixes whatever pages you already have in DB
    so that their titles and slugs in default language are not empty
    and url_path field translations are updated accordingly.
    """

    dependencies = [
        ('wagtailtranslation', '0032_wagtail_translation'),
    ]

    operations = [
        # 1. copy slugs and titles to corresponding default language fields
        migrations.RunSQL(
            ['UPDATE wagtailcore_page SET {}=slug, {}=title'.format(
                build_localized_fieldname('slug', mt_settings.DEFAULT_LANGUAGE),
                build_localized_fieldname('title', mt_settings.DEFAULT_LANGUAGE))],
            migrations.RunSQL.noop),
        # 2. update url_path in all existing pages for all translations
        migrations.RunPython(url_path_fix, migrations.RunPython.noop),
    ]
