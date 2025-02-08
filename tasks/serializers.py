from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_status(self, value):
        """Ensure that the status is one of the predefined choices."""
        if value not in ['todo', 'in_progress', 'done']:
            raise serializers.ValidationError("Invalid status value")
        return value
