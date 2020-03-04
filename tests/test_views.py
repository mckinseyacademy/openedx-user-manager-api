"""
Tests for User Manager Application views
"""
from __future__ import absolute_import, unicode_literals

import json

import ddt
from mock import PropertyMock, patch
from rest_framework.authentication import SessionAuthentication
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from django.test import TestCase

from user_manager.api.v1.views import ManagerViewMixin
from user_manager.models import UserManagerRole

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


@ddt.ddt
class UserManagerRoleViewsTest(TestCase):
    """
    Tests for User Manager Application views
    """

    @staticmethod
    def _create_users():
        """Create regualar test users"""
        for idx in range(10):
            username = 'report{}'.format(idx)
            email = '{username}@somecorp.com'.format(username=username)
            yield User.objects.create(username=username, email=email)

    @staticmethod
    def _create_managers():
        """Create manager test users"""
        for idx in range(2):
            username = 'manager{}'.format(idx)
            email = '{username}@somecorp.com'.format(username=username)
            yield User.objects.create(username=username, email=email)

    def setUp(self):
        super(UserManagerRoleViewsTest, self).setUp()
        self.user = User.objects.create(username='staff', email='staff@example.org', is_staff=True)
        self.user.set_password('test')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.users = list(self._create_users())
        self.managers = list(self._create_managers())
        for user in self.users[:5]:
            UserManagerRole.objects.create(manager_user=self.managers[0], user=user)
        for user in self.users[5:]:
            UserManagerRole.objects.create(manager_user=self.managers[1], user=user)

        UserManagerRole.objects.create(manager_user=self.managers[1], user=self.users[0])

        patcher = patch.object(
            ManagerViewMixin,
            'authentication_classes',
            new_callable=PropertyMock,
            return_value=[SessionAuthentication]
        )
        patcher.start()
        self.addCleanup(patcher.__exit__, None, None, None)

    @ddt.data(
        {'is_staff': False, 'status_code': 403},
        {'is_staff': True, 'status_code': 200},
    )
    @ddt.unpack
    def test_restrict_access_to_staff(self, is_staff, status_code):
        non_staff_user = User.objects.create(
            username='test',
            email='nonstaff@example.org',
            is_staff=is_staff,
        )
        non_staff_user.set_password('test')
        non_staff_user.save()
        client = APIClient()
        client.force_authenticate(user=non_staff_user)
        for url in (
            reverse('v1:managers-list'),
            reverse('v1:manager-reports-list', kwargs={'username': self.managers[0].email}),
            reverse('v1:user-managers-list', kwargs={'username': self.users[0].email})
        ):
            response = client.get(url)
            self.assertEqual(response.status_code, status_code)

    def test_no_duplicate_managers(self):
        response = self.client.get(reverse('v1:managers-list'))
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), 2)

    @ddt.data('username', 'email')
    def test_manager_reports_list_get(self, attr):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': getattr(self.managers[0], attr)},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), 5)

    def test_manager_reports_list_post_multiple(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )

        new_user1 = User.objects.create(username='new_user1', email='new_user1@example.org')
        new_user2 = User.objects.create(username='new_user2', email='new_user2@example.org')
        bad_email = 'notouruser@somedomain.com'
        data = json.dumps([
            {'email': new_user1.email},
            {'username': new_user2.username},
            {'email': bad_email},
        ])
        response = self.client.post(url, data=data, content_type='application/json')
        data = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 202)
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['errors'], [{'detail': 'No user with identifier: {}'.format(bad_email)}])

        query = UserManagerRole.objects.filter(manager_user=self.managers[0])
        self.assertEqual(query.count(), 7)

    def test_manager_reports_list_post_bad_request(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )

        response = self.client.post(url, data={}, content_type='application/json')
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data[0], 'A `username` or `email` must be specified')

    def test_manager_reports_list_post_duplicate(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )
        self.client.post(url, {'email': self.users[0].email})
        query = UserManagerRole.objects.filter(manager_user=self.managers[0])
        self.assertEqual(query.count(), 5)

    def test_manager_reports_list_post_nonexistent(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )

        bad_email = 'non@existent.com'
        response = self.client.post(url, {'email': bad_email, 'id': 11})
        self.assertEqual(response.data, {"detail": "No user with identifier: {}".format(bad_email)})
        self.assertEqual(response.status_code, 404)

    def test_manager_reports_list_delete_all(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        query = UserManagerRole.objects.filter(manager_user=self.managers[0])
        self.assertEqual(query.count(), 0)

    def test_manager_reports_list_delete_single(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )
        response = self.client.delete(
            '{url}?user={email}'.format(url=url, email=self.users[0].email)
        )
        self.assertEqual(response.status_code, 204)
        query = UserManagerRole.objects.filter(manager_user=self.managers[0])
        self.assertEqual(query.count(), 4)
        self.assertNotIn(self.users[0].email, query.values_list('user__email', flat=True))

    def test_manager_reports_list_delete_nonexistent(self):
        url = reverse(
            'v1:manager-reports-list',
            kwargs={'username': self.managers[0].email},
        )
        self.client.delete(
            '{url}?user={email}'.format(url=url, email='non@existent.com')
        )
        query = UserManagerRole.objects.filter(manager_user=self.managers[0])
        self.assertEqual(query.count(), 5)

    @ddt.data('username', 'email')
    def test_user_managers_list_get(self, attr):
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': getattr(self.users[0], attr)},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), 2)

    def test_user_managers_list_post_duplicate(self):
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': self.users[0].email},
        )
        self.client.post(url, {'email': self.managers[0].email})
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 2)

    def test_user_managers_list_post_unregistered(self):
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': self.users[0].email},
        )
        response = self.client.post(url, {'email': 'unregistered@user.com'})
        self.assertEqual(response.status_code, 201)
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 3)
        self.assertIn(
            'unregistered@user.com',
            query.values_list('unregistered_manager_email', flat=True),
        )

    def test_user_managers_list_delete_all(self):
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': self.users[0].email},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 0)

    def test_user_managers_list_delete_single(self):
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 2)
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': self.users[0].email},
        )
        response = self.client.delete(
            '{url}?manager={email}'.format(url=url, email=self.managers[0].email)
        )
        self.assertEqual(response.status_code, 204)
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 1)
        self.assertNotIn(
            self.managers[0].email,
            query.values_list('manager_user__email', flat=True),
        )

    def test_user_managers_list_delete_nonexistent(self):
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 2)
        url = reverse(
            'v1:user-managers-list',
            kwargs={'username': self.users[0].email},
        )
        self.client.delete(
            '{url}?manager={email}'.format(url=url, email='non@existent.com')
        )
        query = UserManagerRole.objects.filter(user=self.users[0])
        self.assertEqual(query.count(), 2)
