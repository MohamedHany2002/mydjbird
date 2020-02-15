
from django.urls import path,include
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.tweets,name='tweets'),
    path('post_tweet/', views.post_tweet,name='post_tweet'),
    path('single_tweet/<int:id>', views.single_tweet,name='single_tweet'),
    path('tweet_comment/', views.tweet_comment,name='tweet_comment'),
    path('tweet_like/<int:id>', views.tweet_like,name='tweet_like'),
    path('tweet_dislike/<int:id>', views.tweet_dislike,name='tweet_dislike'),
    path('tweet_delete/<int:id>', views.delete_tweet,name='delete_tweet'),
    path('edit_tweet/<int:id>', views.edit_tweet,name='edit_tweet'),
    path('follow_user/', views.follow_user,name='follow_user'),
    path('unfollow_user/', views.unfollow_user,name='unfollow_user'),
    path('search_update/<str:keyword>', views.search_update,name='search_update'),
    path('followers/<int:id>', views.user_followers,name='followers'),
    path('followings/<int:id>', views.user_followings,name='followings'),
    path('search/', views.search,name='search'),
    path('notifications/', views.notifications,name='notifications'),


]
