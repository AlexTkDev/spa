from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/create/', PostCreateView.as_view(), name="post_create"),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name="comment_create"),
]
