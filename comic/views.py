from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .models import Comic
from .permissions import IsOwnerOrReadonly
from .serializers import ComicListSerializer, ComicCreateUpdateSerializer, ComicDetailSerializer
from .models import TagChoice


@api_view(('GET',))
def tag_list_api_view(request):
    return Response({'tag': TagChoice}, status=HTTP_200_OK)


class ComicListApiView(ListAPIView):
    serializer_class = ComicListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'slug', 'description', 'tag']
    #  i created this pagination using the PageNumberPagination which
    # i imported from django with just a class
    # pagination_class = PostPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        """ the reason why i comment this is because if there is a
        queryset then we in the class then we are going to use it
        but there is none so i am passing hte queryset in here """
        comic = Comic.objects.all()
        query = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        if query:
            query_list = comic.filter(
                Q(tag__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query) |
                Q(slug__icontains=query) |
                Q(title__icontains=query)
            ).distinct()
        elif tag:
            print(tag)
            query_list = comic.filter(
                Q(tag__icontains=tag)
            ).distinct()
        else:
            query_list = Comic.objects.all()
        return query_list


class ComicDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug=None):
        comic = Comic.objects.get_comic_by_slug(slug)
        if comic:
            comic.view_count += 1
            comic.save()
            serializer = ComicDetailSerializer(comic, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'error': 'Comic does not exist'}, status=HTTP_404_NOT_FOUND)


class ComicCreateApiView(CreateAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ this is to add the user that is creating the post
         to the post """
        serializer.save(user=self.request.user)


class ComicUpdateApiView(RetrieveUpdateAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadonly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ComicDeleteApiView(DestroyAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicListSerializer
    permission_classes = [IsOwnerOrReadonly]
    lookup_field = 'slug'


class ComicRecentApiView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Comic.objects.get_recent_comics()
    serializer_class = ComicListSerializer
    lookup_field = 'slug'


"""
class ComicDetailApiView(RetrieveAPIView):
    queryset = Comic.objects.all()
    serializer_class = ComicDetailSerializer(context={'request': request})
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data.get('id'))
        id_ = serializer.data.get('id')
        item = Comic.objects.get_comic_by_id(id_)
        item.view_count += 1
        item.save()
        return Response(serializer.data)
"""
