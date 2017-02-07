#!/usr/bin/env python
from distutils.core import setup

install_requires = [
    'wagtail>=1.8',
    'django-modeltranslation>=0.12',
]

setup(
    name='wagtail-translation',
    version='0.1.0',
    description='Wagtail CMS translation using django-modeltranslation.',
    long_description=(
        'TBD'
        ),
    author='Tadas Dailyda',
    author_email='tadas@dailyda.com',
    maintainer='Tadas Dailyda',
    maintainer_email='tadas@dailyda.com',
    url='https://github.com/skirsdeda/wagtail-translation',
    packages=[
        'wagtail_translation',
        ],
    package_data={'wagtail_translation': ['static/wagtail_translation/js/*.js']},
    install_requires=install_requires,
    download_url='https://github.com/skirsdeda/wagtail-translation',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License'],
    license='MIT')
