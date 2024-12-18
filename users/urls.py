from django.urls import path
from .views import (
    SignupView, LoginView, CreateMUNView, MUNListView, MUNDetailView, 
    RegistrationView, RegistrationDetailView, PaymentView, DashboardView,
    CommunityListCreateView, CommunityRetrieveUpdateDestroyView, CommunityJoinView,
    PostListCreateView, CommunityPostListCreateView, CommunityMemberListView, CommunityPostListView,
    CommunityEventListCreateView, PostLikeView, CommentListCreateView,
)
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
    path('communities/', CommunityListCreateView.as_view(), name='community_list_create'),
    path('communities/<int:pk>/', CommunityRetrieveUpdateDestroyView.as_view(), name='community_detail'),
    path('communities/<int:pk>/join/', CommunityJoinView.as_view(), name='community_join'),
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('communities/<int:community_id>/posts/', CommunityPostListCreateView.as_view(), name='community_post_list_create'),
    path('communities/<int:community_id>/members/', CommunityMemberListView.as_view(), name='community_member_list'),
    path('communities/<int:community_id>/events/', CommunityEventListCreateView.as_view(), name='community_event_list_create'),
    path('communities/<int:community_id>/posts/', CommunityPostListView.as_view(), name='community_post_list'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post_like'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post_like'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),

]

