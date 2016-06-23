from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'description', 'scheduled_time',
            'last_updated',  'pending', 'user_id'
        )
