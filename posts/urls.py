from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('trending/', views.TrendingPostsView.as_view(), name='trending_posts'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('like/', views.LikePostView.as_view(), name='like_post'),
]