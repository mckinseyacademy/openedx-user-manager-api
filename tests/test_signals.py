"""
Tests for User Manager Application signals
"""
from __future__ import absolute_import, unicode_literals

import mock

from django.contrib.auth.models import User
from django.test import TestCase

from user_manager import signals
from user_manager.models import UserManagerRole


class UserManagerRoleSignalsTest(TestCase):
    """
    Tests for User Manager Application signals
    """

    def setUp(self):
        super(UserManagerRoleSignalsTest, self).setUp()
        self.user = User.objects.create(username='test')
        self.manager_email = 'manager@management.co'
        UserManagerRole.objects.create(
            user=self.user,
            unregistered_manager_email=self.manager_email,
        )

    @mock.patch(
        'user_manager.signals._upgrade_manager_role_entry',
        wraps=signals._upgrade_manager_role_entry,  # pylint: disable=protected-access
    )
    def test_upgrade_user_manager_role(self, mock_upgrade_manager_role_entry):
        query = UserManagerRole.objects.filter(user=self.user)

        self.assertEqual(query.count(), 1)

        user_manager_role = query.get()

        self.assertEqual(user_manager_role.unregistered_manager_email, self.manager_email)
        self.assertIsNone(user_manager_role.manager_user)

        manager = User.objects.create(username='manager', email=self.manager_email)
        query = UserManagerRole.objects.filter(user=self.user)

        self.assertEqual(query.count(), 1)

        user_manager_role = query.get()

        self.assertIsNone(user_manager_role.unregistered_manager_email)
        self.assertEqual(user_manager_role.manager_user, manager)

        mock_upgrade_manager_role_entry.assert_called()
