from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name'
        )


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = (
            'id', 'description', 'scheduled_time', 'last_updated',
            'pending', 'owner'
        )
