#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals

import io
import os
import re
import sys

from setuptools import setup


def get_version(*file_paths):
    u"""
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = io.open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


VERSION = get_version('user_manager', '__init__.py')

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

README = io.open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
CHANGELOG = io.open(os.path.join(os.path.dirname(__file__), 'CHANGELOG.rst')).read()

setup(
    name='openedx-user-manager-api',
    version=VERSION,
    description="""an app that provides a user-manager relationship API in Open edX.""",
    long_description=README + '\n\n' + CHANGELOG,
    author='OpenCraft',
    author_email='help@opencraft.com',
    url='https://github.com/mckinseyacademy/openedx-user-manager-api/',
    packages=[
        'user_manager',
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.11,<2.3",
        "djangorestframework",
        "pytest-django",
    ],
    license="AGPL 3.0",
    zip_safe=False,
    keywords='Django edx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'lms.djangoapp': [
            'user_manager = user_manager.apps:UserManagerAppConfig'
        ],
    }
)
