from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, MUNSerializer, MUNListSerializer, RegistrationSerializer, PaymentSerializer, DashboardDataSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import MUN, Registration, Payment
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

