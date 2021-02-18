from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.db.models import Manager
from django.db.models.signals import pre_save
from django.utils.text import slugify

from comic.models import Comic
from muse_comment.models import Comment

User = settings.AUTH_USER_MODEL


# Create your models here.

class EpisodeManager(Manager):
    def get_episode_by_slug(self, slug):
        item = self.filter(slug=slug).first()
        if item:
            return item
        return None


class Episode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(blank=True, null=True)
    content = models.FileField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    objects = EpisodeManager()

    @property
    def comments(self):
        """ to get the comments on the comment models
        i have created a models manager"""
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def comment_count(self):
        """ to get the comments on the comment models
        i have created a models manager"""
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs.count()

    @property
    def get_content_type(self):
        """
        this is the content type which is used in the form
        :return: the content type of the post :ie , blog | post
        which is the content type of this post
        """
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def get_content_type(self):
        """
        this is the content type which is used in the form
        :return: the content type of the post :ie , blog | post
        which is the content type of this post
        """
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Episode.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug, qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Episode)
