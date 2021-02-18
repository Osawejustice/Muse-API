from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.urls import reverse

UseTypeChoice = (
    ('Publisher', 'Publisher'),
    ('Customer', 'Customer'),
)


# Create your models here.
class User(AbstractUser):
    user_type = models.CharField(max_length=50, choices=UseTypeChoice, default='Customer')

    def __str__(self):
        return self.username


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ProfileManager(Manager):
    def get_publishers_channels(self):
        channels = self.filter(user__user_type__icontains='Publisher')
        print(channels)
        return channels

    def get_publisher_channel(self, username):
        channel = self.filter(user__user_type='Publisher', user__username=username).first()
        print(channel)
        return channel


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200)
    followers = models.ManyToManyField(Follower, related_name='followers',blank=True)
    profileImage = models.ImageField(upload_to='Profile')
    backgroundImage = models.ImageField(upload_to='Background')
    created_date = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username + ' Profile'

    @property
    def profile_follower_count(self):
        return self.followers.all().count()

    @property
    def profile_followers(self):
        return self.followers.all()

    def get_api_url(self):
        return reverse('channel:channel_detail', kwargs={'username': self.user.username})


def post_save_user_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    user_profile, created = Profile.objects.get_or_create(user=instance)
    user_profile.save()


post_save.connect(post_save_user_profile_create, sender=User)
