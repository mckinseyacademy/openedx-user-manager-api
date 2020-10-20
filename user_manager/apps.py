"""
User Manager Application Configuration.
"""
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class UserManagerAppConfig(AppConfig):
    """
    Application Configuration for user_manager.
    """

    name = 'user_manager'
    verbose_name = 'User Manager Application'

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'user-manager-api',
                'regex': r'^api/user_manager/',
                'relative_path': 'api.urls',
            },
        },
    }

    def ready(self):
        """
        Connect signal handlers.
        """
        from . import signals  # pylint: disable=unused-import,import-outside-toplevel
