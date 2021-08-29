from rest_framework import serializers

from .models import Games
from django.contrib.auth import get_user_model

User = get_user_model()

class GameModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Games
        fields = ['id', 'numbers', 'user']

class NewGameResponseSerializer(serializers.Serializer):
    numbers = serializers.ListField()

class NewGameRequestSerializer(serializers.Serializer):
    content = serializers.IntegerField()

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    