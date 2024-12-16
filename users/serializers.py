from rest_framework import serializers
from .models import CustomUser, MUN, Registration, Payment

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

class MUNMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUN
        fields = ['id', 'event_name']

class RegistrationSerializer(serializers.ModelSerializer):
    mun = MUNMinimalSerializer(read_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), source='payment')

    class Meta:
        model = Registration
        fields = ['id', 'mun', 'payment_id', 'custom_fields']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status']
        read_only_fields = ['id', 'status']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'institution']

class DashboardMUNSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUN
        fields = ['id', 'event_name', 'date', 'venue']

class DashboardDataSerializer(serializers.Serializer):
    user = UserProfileSerializer()
    past_muns = DashboardMUNSerializer(many=True)
    registered_muns = DashboardMUNSerializer(many=True)
    upcoming_muns = DashboardMUNSerializer(many=True)