from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from comic_episode.models import Episode
from muse_comment.serializers import CommentSerializer
from users.serializers import UserDetailSerializer

episode_delete_url = HyperlinkedIdentityField(
    read_only=True,
    view_name='episode_api:episode_delete',
    lookup_field='slug'
)
episode_update_url = HyperlinkedIdentityField(
    read_only=True,
    view_name='episode_api:episode_update',
    lookup_field='slug'
)

episode_detail_url = HyperlinkedIdentityField(
    read_only=True,
    view_name='episode_api:episode_detail',
    lookup_field='slug'
)


class EpisodeSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    episode_delete_url = episode_delete_url

    episode_update_url = episode_update_url
    episode_detail_url = episode_detail_url
    comment_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Episode
        read_only_true = [
            'timestamp',
            'view_count',
            'episode_delete_url',
            'episode_update_url',
            'episode_detail_url',
            'comment_count',

        ]
        fields = [
            'title',
            'user',
            'thumbnail',
            'content',
            'view_count',
            'comments',
            'comment_count',
            'timestamp',
            'episode_delete_url',
            'episode_update_url',
            'episode_detail_url',
        ]

    def get_comment_count(self, obj):
        return obj.comment_count


class EpisodeDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    episode_delete_url = episode_delete_url

    episode_update_url = episode_update_url
    comment_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Episode
        read_only_true = [
            'timestamp',
            'view_count',
            'episode_delete_url',
            'episode_update_url',
            'comment_count',
            'comments'

        ]
        fields = [
            'title',
            'user',
            'thumbnail',
            'content',
            'view_count',
            'comments',
            'comment_count',
            'timestamp',
            'episode_delete_url',
            'episode_update_url',
        ]

    def get_comment_count(self, obj):
        return obj.comment_count

    def get_comment(self, obj):
        comments = CommentSerializer(obj.comments, many=True,
                                     context={'request': self.context['request']}).data
        return comments


class EpisodeCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'user',
            'title',
            'thumbnail',
            'content',
            'timestamp',
            'comic',
        ]
