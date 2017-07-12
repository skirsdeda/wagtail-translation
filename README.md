# wagtail-translation

**wagtail-translation** adds translation capabilities to [Wagtail CMS](https://github.com/wagtail/wagtail) 
by using [django-modeltranslation](https://github.com/deschler/django-modeltranslation).
The aim is to have a very clean implementation of single-tree Wagtail translations.
This project was inspired by [wagtail-modeltranslation](https://github.com/infoportugal/wagtail-modeltranslation)
because it is unnecessarily messy and not very maintainable.

## Installation

1. Add `wagtail_translation` and `modeltranslation` to `INSTALLED_APPS` in your settings.
   `wagtail_translation` must appear before any apps with subclassed Page models in the list.
2. Define languages used for translations (see modeltranslation docs).
3. Define and register `TranslationOptions` classes for every Page model.
   If said models don't have any additional fields to be translated, they still have to be registered
   with empty `TranslationOptions`.
4. Run ```./manage.py migrate```.

   TBD: additional actions to install in preexisting projects (which had migrations run before)

   TBD: additional actions when translation languages are changed after running wagtail-translation migration
5. If you have custom managers on your `Page` submodels, make sure that such managers inherit from
   `wagtail_translation.manager.MultilingualPageManager`.
   
### Dependencies and versions

| Dependency              | Versions    |
|-------------------------|-------------|
| wagtail                 | >=1.8,<1.12 |
| django-modeltranslation | >=0.12      |
| django                  | >=1.8,<2.0  |

## Configuration

1. Include wagtail urls with i18n_patterns
2. Add LocaleMiddleware to middleware list in your settings.
