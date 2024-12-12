from django.urls import path
from .views import SignupView, LoginView, CreateMUNView, MUNListView, MUNDetailView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('muns/create/', CreateMUNView.as_view(), name='create_mun'),
    path('muns/', MUNListView.as_view(), name='mun_list'),
    path('muns/<int:pk>/', MUNDetailView.as_view(), name='mun_detail'),
]

