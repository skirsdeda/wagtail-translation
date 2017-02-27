from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from .utils import obj_per_lang


# add localized titles to search index (this is used as patched Page.search_fields)
search_fields = (
    # for now original 'title' field is left intact
    Page.search_fields +
    obj_per_lang(index.SearchField, 'title', partial_match=True, boost=2)
)
