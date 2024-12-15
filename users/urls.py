from django.urls import path
from .views import SignupView, LoginView, CreateMUNView, MUNListView, MUNDetailView, RegistrationView, RegistrationDetailView, PaymentView, DashboardView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('muns/create/', CreateMUNView.as_view(), name='create_mun'),
    path('muns/', MUNListView.as_view(), name='mun_list'),
    path('muns/<int:pk>/', MUNDetailView.as_view(), name='mun_detail'),
    path('registrations/', RegistrationView.as_view(), name='registration'),
    path('registrations/<int:pk>/', RegistrationDetailView.as_view(), name='registration_detail'),
    path('payments/', PaymentView.as_view(), name='payment'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

