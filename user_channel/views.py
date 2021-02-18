from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from user_channel.serializers import ChannelDetailSerializer, ChannelListSerializer
from users.models import Profile


class ChannelListView(ListAPIView):
    serializer_class = ChannelListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__last_name', 'about']
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        """ the reason why i comment this is because if there is a
        queryset then we in the class then we are going to use it
        but there is none so i am passing hte queryset in here """
        channel = Profile.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = channel.filter(
                Q(user__username__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(about__icontains=query)
            ).distinct()
        else:
            query_list = Profile.objects.get_publishers_channels()
        return query_list


class ChannelDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username=None):
        print('this is the username', username)
        publisher = Profile.objects.get_publisher_channel(username)
        print(publisher)
        if publisher:
            serializer = ChannelDetailSerializer(publisher)
            print(serializer)
            print(serializer.data)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # user must be logged in
def channel_follow(request, *args, **kwargs):
    username = request.POST.get('username')
    if request.user != username:
        profile = Profile.objects.get_publisher_channel(username)
        if not username in profile.followers.all():
            profile.followers.add(username)
            return Response({'message': f'You just started following {username}'}, status=HTTP_200_OK)
        return Response({'error': 'This channel does not exist'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'There was an error'}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # user must be logged in
def channel_unfollow(request, *args, **kwargs):
    username = request.POST.get('username')
    if request.user != username:
        profile = Profile.objects.get_publisher_channel(username)
        if profile:
            if username in profile.followers.all():
                print('the user followers', profile.followers.all())
                profile.followers.remove(username)
                return Response({'message': f'You have successfully unfollow {username}'}, status=HTTP_200_OK)
            return Response({'error': 'You are not following '}, status=HTTP_404_NOT_FOUND)
        return Response({'error': 'This channel does not exist'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'There was an error'}, status=HTTP_400_BAD_REQUEST)
