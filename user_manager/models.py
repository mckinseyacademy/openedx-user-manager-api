"""
Models for User Manager Application.
"""
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class UserManagerRole(models.Model):
    """
    Creates a manager-managee link between users.

    .. note::
        In case the manager doesn't have an account registered in the system,
        their email will be linked instead, and auto-upgraded to a foreign key
        when they register an account.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
    )
    manager_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
    )
    # This will get upgraded to a foreign key to the manager's user account
    # when they register.
    unregistered_manager_email = models.EmailField(
        # This field is part of a unique_together constraint with ``user`` so it
        # needs to have ``null=True`` despite being backed by a CharField.
        null=True,
        blank=True,
        help_text="The email address for a manager if they haven't currently "
                  "registered for an account."
    )

    class Meta(object):  # pylint: disable=useless-object-inheritance
        """
        Meta settings for ``UserManagerRole`` object.
        """

        app_label = 'user_manager'
        ordering = ['manager_user']
        unique_together = (
            ('user', 'manager_user'),
            ('user', 'unregistered_manager_email'),
        )

    def __str__(self):
        """
        Readable name for ``UserManagerRole`` object.
        """
        return '{user} reports to {manager}'.format(
            user=self.user.email,
            manager=self.manager_email,
        )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Validate and save ``UserManagerRole`` object.
        """
        self.full_clean()
        super(UserManagerRole, self).save(force_insert, force_update, using, update_fields)

    @property
    def manager_email(self):
        """
        Get manager email for registered or unregistered manager.
        """
        if self.manager_user:
            return self.manager_user.email
        else:
            return self.unregistered_manager_email

    def clean(self):
        """
        Validate ``UserManagerRole`` object.
        """
        if (
                self.user == self.manager_user or self.user.email == self.unregistered_manager_email
        ):
            raise ValidationError('User cannot be own manager')
