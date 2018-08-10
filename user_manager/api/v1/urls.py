"""
API URLs for User Manager Application
"""
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url

from . import views

app_name = "user_manager"

urlpatterns = [
    url(
        r'^managers/$',
        views.ManagerListView.as_view(),
        name='managers-list',
    ),
    url(
        r'^users/{}/managers/$'.format(settings.USERNAME_PATTERN),
        views.UserManagerListView.as_view(),
        name='user-managers-list',
    ),
    url(
        r'^managers/{}/reports/$'.format(settings.USERNAME_PATTERN),
        views.ManagerReportsListView.as_view(),
        name='manager-reports-list',
    ),
]
