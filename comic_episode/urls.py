from django.urls import path

from .views import (EpisodeCreateApiView, EpisodeListApiView, EpisodeDetailApiView, EpisodeUpdateApiView,
                    EpisodeDeleteApiView
                    )

app_name = 'episode_api'
urlpatterns = [
    path('episode/', EpisodeListApiView.as_view(), name='episode_list'),
    path('episode_create/', EpisodeCreateApiView.as_view(), name='episode_create'),
    path('episode/<str:slug>/', EpisodeDetailApiView.as_view(), name='episode_detail'),
    path('episode/<str:slug>/update/', EpisodeUpdateApiView.as_view(), name='episode_update'),
    path('episode/<str:slug>/delete/', EpisodeDeleteApiView.as_view(), name='episode_delete'),

]
