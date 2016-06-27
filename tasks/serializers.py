from rest_framework import serializers

from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'firstname', 'lastname',
            'password', 'email_verified'
        )


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = (
            'id', 'description', 'scheduled_time', 'last_updated',
            'pending', 'user'
        )
