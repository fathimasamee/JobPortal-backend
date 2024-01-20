from django.contrib.auth.models import User
from rest_framework import serializers

from .models import JobSeeker

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

class jobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = '__all__'

