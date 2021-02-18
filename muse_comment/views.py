from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import Comment
from .serializers import CommentSerializer, create_comment_serializer, CommentDeleteUpdateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import Comment
from .serializers import CommentSerializer, create_comment_serializer, CommentDeleteUpdateSerializer


class CommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    serializer_class = CommentSerializer


class CommentDetailApiView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    serializer_class = CommentSerializer


class CommentCreateApiView(CreateAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    """ i am using the serializer class i created on the serializer"""

    def get_serializer_class(self):
        model_type = self.request.POST.get('type')
        slug = self.request.POST.get('slug')
        parent_id = self.request.POST.get('parent_id', None)
        print('these are the values', model_type, slug, parent_id)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )


class CommentUpdateApiView(RetrieveUpdateAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'id'


class CommentDeleteApiView(RetrieveUpdateDestroyAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'id'
