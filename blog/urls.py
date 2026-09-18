from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/new/', views.post_create_view, name='post_create'),

    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('post/<int:pk>/edit/', views.post_edit_view, name='post_edit'),

]