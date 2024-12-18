from rest_framework import serializers
from .models import CustomUser, MUN, Registration, Payment, Community, Post, Event, Comment

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


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'creator', 'members', 'created_at']
        read_only_fields = ['id', 'creator', 'members', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'community', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def get_author_name(self, obj):
        return obj.author.username

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'community', 'name', 'date', 'description']
        read_only_fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def get_author_name(self, obj):
        return obj.author.username

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'community', 'content', 'created_at', 'likes_count', 'comments', 'is_liked']
        read_only_fields = ['id', 'author', 'created_at', 'likes_count', 'comments', 'is_liked']

    def get_author_name(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

