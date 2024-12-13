from rest_framework import serializers
from .models import CustomUser, MUN

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'username', 'gender', 'date_of_birth', 'contact_number', 'institution', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class MUNSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUN
        fields = ['id', 'event_name', 'date', 'venue', 'description' ,'registration_fees', 'custom_fields']
        read_only_fields = ['id']

    def create(self, validated_data):
        return MUN.objects.create(**validated_data)

class MUNListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUN
        fields = ['id', 'event_name', 'date', 'venue', 'registration_fees']

