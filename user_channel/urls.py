from django.contrib import admin
from django.urls import path
from .views import ChannelListView, ChannelDetailView, channel_follow, channel_unfollow

app_name = 'channel'
urlpatterns = [
    path('channel/', ChannelListView.as_view(), name='channel_list'),
    path('channel_follow/', channel_follow, name='channel_follow'),
    path('channel_unfollow/', channel_unfollow, name='channel_unfollow'),

    path('channel/<str:username>/', ChannelDetailView.as_view(), name='channel_detail'),

]
