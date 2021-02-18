from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from muse_comment.models import Comment

User = settings.AUTH_USER_MODEL

TagChoice = (
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Romance', 'Romance'),
)


class ComicManger(models.Manager):
    def get_recent_comics(self):
        last_seven_days = timedelta(days=7)
        day = datetime.now(tz=timezone.utc) - last_seven_days
        comic_qs = self.filter(timestamp__gte=day).order_by('?')
        print(comic_qs)
        return comic_qs

    def get_publisher_recent_comics(self, user):
        last_seven_days = timedelta(days=7)
        day = datetime.now(tz=timezone.utc) - last_seven_days
        comic_qs = self.filter(timestamp__gte=day, user=user).order_by('?')
        print(comic_qs)
        return comic_qs

    def get_comic_by_id(self, id):
        item = self.filter(id=id).first()
        if item:
            return item
        return None

    def get_comic_by_slug(self, slug):
        item = self.filter(slug=slug).first()
        if item:
            return item
        return None


class Comic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=20, choices=TagChoice)
    view_count = models.IntegerField(default=0)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField()
    objects = ComicManger()

    def __str__(self):
        return str(self.timestamp)

    @property
    def episodes(self):
        return self.episode_set.all()

    @property
    def episode_count(self):
        return self.episode_set.all().count()

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

    def get_api_url(self):
        return reverse('comic_ap:detail', kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Comic.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug, qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Comic)
