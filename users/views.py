from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, MUNSerializer, MUNListSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import MUN, Registration

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
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationDetailView(generics.RetrieveAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Implement payment processing logic here
        # For now, we'll just return a success response
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

