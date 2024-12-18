from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    UserSerializer, MUNSerializer, MUNListSerializer, RegistrationSerializer, 
    PaymentSerializer, DashboardDataSerializer, CommunitySerializer, 
    PostSerializer, EventSerializer, PostSerializer, CommentSerializer, ContactMessageSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import MUN, Registration, Payment, Community, Post, Event, Comment,  ContactMessage
from django.utils import timezone

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateMUNView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MUNSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MUNListView(generics.ListAPIView):
    queryset = MUN.objects.all()
    serializer_class = MUNListSerializer

class MUNDetailView(generics.RetrieveAPIView):
    queryset = MUN.objects.all()
    serializer_class = MUNSerializer

class RegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({'error': 'Invalid payment ID'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save(user=request.user, payment=payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationDetailView(generics.RetrieveAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(user=request.user)
            return Response({'payment_id': payment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()

        registered_muns = MUN.objects.filter(
            registration__user=user, 
            date__gte=now
        ).distinct().values('id', 'event_name', 'date', 'venue')

        past_muns = MUN.objects.filter(
            registration__user=user, 
            date__lt=now
        ).distinct().values('id', 'event_name', 'date', 'venue')

        upcoming_muns = MUN.objects.filter(
            date__gte=now
        ).exclude(
            id__in=registered_muns.values_list('id', flat=True)
        ).values('id', 'event_name', 'date', 'venue')[:5]  # Limit to 5 upcoming MUNs

        dashboard_data = {
            'user': {
                'full_name': user.full_name,  # Assuming the user model has a full_name field
                'email': user.email,
                'institution': user.institution
            },
            'past_muns': list(past_muns),
            'registered_muns': list(registered_muns),
            'upcoming_muns': list(upcoming_muns)
        }

        serializer = DashboardDataSerializer(dashboard_data)
        return Response(serializer.data)
    
class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = []  # Allow unauthenticated access for GET

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = Community.objects.all()
        joined = self.request.query_params.get('joined', None)
        if joined is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(members=self.request.user)
        return queryset


class CommunityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != request.user:
            return Response({"error": "You are not allowed to update this community"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != request.user:
            return Response({"error": "You are not allowed to delete this community"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class CommunityJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            community = Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user in community.members.all():
            return Response({"error": "You are already a member of this community"}, status=status.HTTP_400_BAD_REQUEST)

        community.members.add(request.user)
        return Response({"success": "You have joined the community"}, status=status.HTTP_200_OK)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(community__isnull=True)
    serializer_class = PostSerializer
    permission_classes = []  # Allow unauthenticated access for GET

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CommunityPostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Post.objects.filter(community_id=community_id)

    def perform_create(self, serializer):
        community_id = self.kwargs['community_id']
        community = Community.objects.get(pk=community_id)
        serializer.save(author=self.request.user, community=community)

class CommunityMemberListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Community.objects.get(pk=community_id).members.all()

class CommunityEventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Event.objects.filter(community_id=community_id)

    def perform_create(self, serializer):
        community_id = self.kwargs['community_id']
        community = Community.objects.get(pk=community_id)
        serializer.save(community=community)


class CommunityPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Post.objects.filter(community_id=community_id).order_by('-created_at')

class CommunityPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Post.objects.filter(community_id=community_id).order_by('-created_at')


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({"liked": False}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({"liked": True}, status=status.HTTP_200_OK)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


class ContactMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your message has been sent successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

