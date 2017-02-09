from __future__ import absolute_import, unicode_literals

import logging
from modeltranslation import settings as mt_settings
from django import VERSION as DJANGO_VERSION
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from modeltranslation.utils import build_localized_fieldname, get_translation_fields
from wagtail.wagtailcore.models import Page, Site

from .edit_handlers import content_panels as _content_panels
from .edit_handlers import promote_panels as _promote_panels

logger = logging.getLogger('wagtail.core')

__all__ = ['set_url_path', '_lang_slug_is_available', '_get_autogenerated_lang_slug',
           'full_clean', 'clean', 'save', '_update_descendant_lang_url_paths',
           'move', 'content_panels', 'promote_panels']


def set_url_path(self, parent):
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        url_path_attr = build_localized_fieldname('url_path', lang_code)
        slug_attr = build_localized_fieldname('slug', lang_code)
        if parent:
            # When slug has no translation, added url_path part will become '//'
            # which will make this page not accessible in this language
            # because wagtail urls will simply not match it.
            # On the other hand, non empty url_path for every language is important.
            # It makes sure descendant url_path updating keeps working as expected.
            slug = getattr(self, slug_attr, '') or ''
            new_url_path = getattr(parent, url_path_attr) + slug + '/'
        else:
            new_url_path = '/'
        setattr(self, url_path_attr, new_url_path)

    return self.url_path  # return current language url_path

@staticmethod
def _lang_slug_is_available(slug, lang_code, parent_page, page=None):
    if parent_page is None:
        return True

    siblings = parent_page.get_children()
    if page:
        siblings = siblings.not_page(page)

    slug_f = build_localized_fieldname('slug', lang_code)
    return not siblings.filter(**{slug_f: slug}).exists()

def _get_autogenerated_lang_slug(self, base_slug, lang_code):
    candidate_slug = base_slug
    suffix = 1
    parent_page = self.get_parent()
    cls = type(self)

    while not cls._lang_slug_is_available(candidate_slug, lang_code, parent_page, self):
        suffix += 1
        candidate_slug = "%s-%d" % (base_slug, suffix)

    return candidate_slug

def full_clean(self, *args, **kwargs):
    # autogenerate slugs for non-empty title translation
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        title_field = build_localized_fieldname('title', lang_code)
        slug_field = build_localized_fieldname('slug', lang_code)

        title = getattr(self, title_field)
        slug = getattr(self, slug_field)
        if title and not slug:
            if DJANGO_VERSION >= (1, 9):
                base_slug = slugify(title, allow_unicode=True)
            else:
                base_slug = slugify(title)

            if base_slug:
                setattr(self, slug_field, self._get_autogenerated_lang_slug(base_slug, lang_code))

    super(Page, self).full_clean(*args, **kwargs)

def clean(self):
    errors = {}
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        slug_field = build_localized_fieldname('slug', lang_code)
        slug = getattr(self, slug_field)
        cls = type(self)
        if slug and not cls._lang_slug_is_available(slug, lang_code, self.get_parent(), self):
            errors[slug_field] = _("This slug is already in use")
    if errors:
        raise ValidationError(errors)

@transaction.atomic
def save(self, *args, **kwargs):
    self.full_clean()

    update_descendant_url_paths = False
    is_new = self.id is None

    if is_new:
        self.set_url_path(self.get_parent())
    elif 'update_fields' in kwargs:
        slug_fields = get_translation_fields('slug')
        updated_slug_fields = [f for f in slug_fields if f in kwargs['update_fields']]
        if updated_slug_fields:
            old_record = Page.objects.get(id=self.id)
            if any(getattr(old_record, f) != getattr(self, f) for f in updated_slug_fields):
                self.set_url_path(self.get_parent())
                update_descendant_url_paths = True

    result = super(Page, self).save(*args, **kwargs)

    if update_descendant_url_paths:
        self._update_descendant_lang_url_paths(old_record)

    if Site.objects.filter(root_page=self).exists():
        cache.delete('wagtail_site_root_paths')

    if is_new:
        cls = type(self)
        logger.info(
            "Page created: \"%s\" id=%d content_type=%s.%s path=%s",
            self.title,
            self.id,
            cls._meta.app_label,
            cls.__name__,
            self.url_path
        )

    return result

def _update_descendant_lang_url_paths(self, old_page):
    cursor = connection.cursor()
    if connection.vendor == 'sqlite':
        field_update_fmt = "{0} = %s || substr({0}, %s)"
    elif connection.vendor == 'mysql':
        field_update_fmt = "{0} = CONCAT(%s, substring({0}, %s))"
    elif connection.vendor in ('mssql', 'microsoft'):
        field_update_fmt = "{0} = CONCAT(%s, (SUBSTRING({0}, 0, %s)))"
    else:
        field_update_fmt = "{0} = %s || substring({0} from %s)"

    exec_args = []
    update_fields_sql = []
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        url_path_attr = build_localized_fieldname('url_path', lang_code)
        new_url_path = getattr(self, url_path_attr)
        old_url_path = getattr(old_page, url_path_attr)
        if new_url_path != old_url_path:
            update_fields_sql.append(field_update_fmt.format(url_path_attr))
            exec_args.append(new_url_path)
            exec_args.append(len(old_url_path) + 1)

    update_sql = """
    UPDATE wagtailcore_page
    SET {} WHERE path LIKE %s AND id <> %s
    """.format(','.join(update_fields_sql))
    exec_args.append(self.path + '%')
    exec_args.append(self.id)
    cursor.execute(update_sql, exec_args)

@transaction.atomic
def move(self, target, pos=None):
    old_self = Page.objects.get(id=self.id)
    super(Page, self).move(target, pos=pos)

    new_self = Page.objects.get(id=self.id)
    # go through slugs to make sure they're available in new parent
    # and auto-update if necessary
    for lang_code in mt_settings.AVAILABLE_LANGUAGES:
        slug_attr = build_localized_fieldname('slug', lang_code)
        slug = getattr(new_self, slug_attr)
        if slug:
            slug = new_self._get_autogenerated_lang_slug(slug, lang_code)
            setattr(new_self, slug_attr, slug)
    new_self.set_url_path(new_self.get_parent())
    new_self.save()
    new_self._update_descendant_lang_url_paths(old_self)

    logger.info("Page moved: \"%s\" id=%d path=%s", self.title, self.id, self.url_path)

content_panels = _content_panels
promote_panels = _promote_panels
