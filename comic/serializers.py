from django.http import request
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from comic.models import Comic
from muse_comment.serializers import CommentSerializer
from comic_episode.serializers import EpisodeSerializer
from users.serializers import UserDetailSerializer

comic_delete_url = HyperlinkedIdentityField(
    view_name='comic_api:comic_delete',
    lookup_field='slug'
)
comic_update_url = HyperlinkedIdentityField(
    view_name='comic_api:comic_update',
    lookup_field='slug'
)

comic_detail_url = HyperlinkedIdentityField(
    view_name='comic_api:comic_detail',
    lookup_field='slug'
)


class ComicListSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    episode_count = SerializerMethodField(read_only=True)
    comment_count = SerializerMethodField(read_only=True)
    comic_detail_url = comic_detail_url
    comic_delete_url = comic_delete_url
    comic_update_url = comic_update_url

    class Meta:
        model = Comic
        read_only_fields = [
            'episode_count',
            'comment_count',
        ]
        fields = [
            'user',
            'title',
            'tag',
            'slug',
            'view_count',
            'description',
            'timestamp',
            'thumbnail',
            'episode_count',
            'comment_count',
            'comic_detail_url',
            'comic_delete_url',
            'comic_update_url',
        ]

    def get_episode_count(self, obj):
        return obj.episode_count

    def get_comment_count(self, obj):
        return obj.comment_count


class ComicDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    episode = SerializerMethodField(read_only=True)
    episode_count = SerializerMethodField(read_only=True)

    comment = SerializerMethodField(read_only=True)
    comment_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Comic
        read_only_fields = [
            'user',
            'id',
            'slug',
            'view_count',
            'timestamp',
            'episode',
            'episode_count',
            'comment',
            'comment_count',
        ]
        fields = [
            'id',
            'slug',
            'user',
            'title',
            'tag',
            'view_count',
            'description',
            'timestamp',
            'thumbnail',
            'episode_count',
            'episode',
            'comment',
            'comment_count',
        ]

    def get_episode_count(self, obj):
        return obj.episode_count

    def get_episode(self, obj):
        episodes = EpisodeSerializer(obj.episodes, many=True,
                                     context={'request': self.context['request']}).data
        return episodes

    def get_comment_count(self, obj):
        return obj.comment_count

    def get_comment(self, obj):
        comments = CommentSerializer(obj.comments, many=True,
                                     context={'request': self.context['request']}).data
        return comments


class ComicCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comic
        fields = [
            'title', 'tag', 'description', 'thumbnail'
        ]
