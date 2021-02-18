from django.urls import path

from .views import (CommentCreateApiView, CommentListApiView, CommentDetailApiView, CommentUpdateApiView,
                    CommentDeleteApiView
                    )

app_name = 'comment_api'
urlpatterns = [
    path('', CommentListApiView.as_view(), name='comment_list'),
    path('comment_create/', CommentCreateApiView.as_view(), name='comment_create'),
    path('<int:id>/', CommentDetailApiView.as_view(), name='comment_detail'),
    path('<int:id>/update/', CommentUpdateApiView.as_view(), name='comment_update'),
    path('<int:id>/delete/', CommentDeleteApiView.as_view(), name='comment_delete'),

]
