from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='landing'),
    path('job_search/', views.job_search, name='job_search'),
    path('api/trending-news/', views.get_trending_news, name='trending-news'),
    path('api/breaking-news/', views.get_breaking_news, name='breaking-news'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('loading', views.load, name='load'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user_profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
