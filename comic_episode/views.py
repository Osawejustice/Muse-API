from django.shortcuts import render
from rest_framework import request
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .models import Episode
from .serializers import EpisodeCreateUpdateSerializer, EpisodeSerializer, EpisodeDetailSerializer


class EpisodeListApiView(ListAPIView):
    queryset = Episode.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    serializer_class = EpisodeSerializer


class EpisodeDetailApiView(RetrieveDestroyAPIView):
    queryset = Episode.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    serializer_class = EpisodeDetailSerializer(context={'request': request})

class EpisodeDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug=None):
        comic = Episode.objects.get_episode_by_slug(slug)
        if comic:
            comic.view_count += 1
            comic.save()
            serializer = EpisodeDetailSerializer(comic, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'error': 'episode does not exist'}, status=HTTP_404_NOT_FOUND)

class EpisodeCreateApiView(CreateAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Episode.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EpisodeCreateUpdateSerializer
    lookup_field = 'slug'


class EpisodeUpdateApiView(RetrieveUpdateAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Episode.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EpisodeCreateUpdateSerializer
    lookup_field = 'slug'


class EpisodeDeleteApiView(RetrieveUpdateDestroyAPIView):
    """ this si not doing all the comment s it is only doing the
     parent comment because we override it in our comment manager """
    queryset = Episode.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EpisodeCreateUpdateSerializer
    lookup_field = 'slug'
