from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/new/', views.post_create_view, name='post_create')
]