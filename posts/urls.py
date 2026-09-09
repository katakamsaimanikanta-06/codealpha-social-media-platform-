from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<int:post_id>/like/', views.like_toggle_view, name='like_toggle'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
]
