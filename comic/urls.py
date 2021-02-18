from django.urls import path

from .views import (
    ComicListApiView, ComicDetailApiView, ComicUpdateApiView, ComicDeleteApiView, ComicCreateApiView,
    ComicRecentApiView, tag_list_api_view
)

app_name = 'comic_api'
urlpatterns = [
    path('comic/', ComicListApiView.as_view(), name='comic_list'),
    path('comic_recent/', ComicRecentApiView.as_view(), name='comic_recent'),
    path('comic_tags/', tag_list_api_view, name='comic_tags'),
    path('comic/<str:slug>/', ComicDetailApiView.as_view(), name='comic_detail'),
    path('comic/<str:slug>/delete/', ComicDeleteApiView.as_view(), name='comic_delete'),
    path('comic/<str:slug>/update/', ComicUpdateApiView.as_view(), name='comic_update'),
    path('comic_create/', ComicCreateApiView.as_view(), name='comic_create'),

]
