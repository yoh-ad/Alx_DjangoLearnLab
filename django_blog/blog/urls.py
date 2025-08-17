from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    register, profile, PostsByTagView, SearchResultsView
)

urlpatterns = [
    # Posts
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comments
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tags and Search
    path('tags/<str:tag_name>/', PostsByTagView.as_view(), name='posts_by_tag'),
    path('search/', SearchResultsView.as_view(), name='search'),

    # Auth (registration & profile; login/logout provided by accounts/ include)
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
