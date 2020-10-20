"""
Serializers for User Manager Application
"""
from __future__ import absolute_import, unicode_literals

from rest_framework import fields, serializers

from django.core.validators import EmailValidator

from ...utils import create_user_manager_role


class ManagerListSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """ Serializer for User manager """

    email = fields.SerializerMethodField(validators=(EmailValidator,))
    username = fields.SerializerMethodField()

    class Meta(object):  # pylint: disable=useless-object-inheritance
        fields = ('email', 'username')

    def get_email(self, obj):
        """
        Get email from object dict.
        """
        if obj["manager_user__username"] is not None:
            return obj["manager_user__email"]
        else:
            return obj["unregistered_manager_email"]

    def get_username(self, obj):
        """
        Get manager username from object dict.
        """
        return obj["manager_user__username"]


class ManagerReportsSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """ Serializer for User manager reports """

    id = fields.IntegerField(source='user.id', required=False)
    email = fields.EmailField(source='user.email', required=False)
    username = fields.CharField(source='user.username', required=False)

    def create(self, validated_data):
        """
        Create UserManagerRole object.
        """
        user = validated_data.get('user')
        manager_user = validated_data.get('manager_user')
        unregistered_manager_email = validated_data.get('unregistered_manager_email')
        return create_user_manager_role(user, manager_user, unregistered_manager_email)


class UserManagerSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """ Serializer for User manager reports """

    email = fields.EmailField(source='manager_email')
    username = fields.CharField(source='manager_user.username', required=False)

    def create(self, validated_data):
        """
        Create UserManagerRole object.
        """
        user = validated_data.get('user')
        manager_user = validated_data.get('manager_user')
        unregistered_manager_email = validated_data.get('unregistered_manager_email')
        return create_user_manager_role(user, manager_user, unregistered_manager_email)
