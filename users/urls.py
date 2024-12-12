from django.urls import path
from .views import SignupView, LoginView, CreateMUNView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('muns/create/', CreateMUNView.as_view(), name='create_mun'),
]