from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from comic.models import Comic
from comic.serializers import ComicListSerializer
from users.models import Profile, User, Follower
from users.serializers import UserDetailSerializer, StringSerializer

channel_detail_url = HyperlinkedIdentityField(
    view_name='channel:channel_detail', source=User,
    lookup_field='username', read_only=True
)


class FollowerSerializer(ModelSerializer):
    user = StringSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = [
            'user',
            'timestamp',
        ]


class ChannelListSerializer(ModelSerializer):
    user = StringSerializer(read_only=True)
    follower_count = SerializerMethodField(read_only=True)
    channel_detail_url = channel_detail_url

    class Meta:
        model = Profile
        fields = [
            'id',
            'channel_detail_url',
            'follower_count',
            'about',
            'profileImage',
            'backgroundImage',
            'user',
        ]

    def get_follower_count(self, obj):
        return obj.profile_follower_count


# FollowerSerializer
class ChannelDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    followers = SerializerMethodField(read_only=True)
    comics = SerializerMethodField(read_only=True)
    recent_comics = SerializerMethodField(read_only=True)
    most_viewed_comics = SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'about',
                  'profileImage',
                  'followers',
                  'comics',
                  'recent_comics',
                  'most_viewed_comics',
                  )

    def get_followers(self, obj):
        serializer = FollowerSerializer(obj.profile_followers, many=True)
        return serializer.data

    def get_comics(self, obj):
        comic = Comic.objects.filter(user=obj.user)
        print('this is the comic', comic)
        serializer = ComicListSerializer(comic, many=True)
        return serializer.data

    def get_recent_comics(self, obj):
        comic = Comic.objects.get_publisher_recent_comics(user=obj.user)
        serializer = ComicListSerializer(comic, many=True)
        return serializer.data

    def get_most_viewed_comics(self, obj):
        comic = Comic.objects.filter(user=obj.user).order_by('-view_count')
        serializer = ComicListSerializer(comic, many=True)
        return serializer.data
