from django.urls import path

from .views import PostCreateView, PostDetailView, PostListView, about, home

app_name = "blog"

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
]