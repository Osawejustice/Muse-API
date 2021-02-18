from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.relations import HyperlinkedIdentityField

from .models import Profile
from .models import User, UseTypeChoice
from rest_framework.serializers import (
    ModelSerializer, EmailField, CharField
)


class StringSerializer(serializers.StringRelatedField):

    def to_internal_value(self, data):
        return value


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id',
                  'user',
                  'about',
                  'followers',
                  'profileImage',
                  )


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id',
                  'about',
                  'profileImage',
                  'followers',
                  )


user_detail_serializer = HyperlinkedIdentityField(
    view_name='user',
    lookup_field='username', read_only=True, source=User
)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileUserSerializer()
    user_detail_serializer = user_detail_serializer

    class Meta:
        model = User
        read_only_fields = [
            'password', 'id','user_detail_serializer',
        ]
        fields = ('id',
                  'user_detail_serializer',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'password',
                  'user_type',
                  'profile',)

    # i dont know but it is not working
    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile')
        user_objects = {
            'data': validated_data
        }
        print('users objects', user_objects)
        # user = User.objects.create(**validated_data)
        user = User()
        user.username = validated_data.get('username')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.email = validated_data.get('email')
        user.user_type = validated_data.get('user_type')
        user.set_password(validated_data.get('password'))
        user.save()
        profile_data = {
            'data': profile_data
        }
        print('profile_data', profile_data)
        # i am defining a post save in the profile model for the user
        # Profile.objects.create(user=user, **profile_data)
        return user

    # using it to update the user profile
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        profile = instance.profile
        print('instance profile', instance.profile)
        print('instance user', instance)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.save()

        profile.user = instance
        profile.profileImage = profile_data.get(
            'profileImage',
            profile.profileImage
        )
        profile.backgroundImage = profile_data.get(
            'backgroundImage',
            profile.backgroundImage
        )
        profile.about = profile_data.get(
            'about',
            profile.about
        )
        profile.save()
        return instance


class CustomRegisterSerializer(RegisterSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'username',
                  'password1',
                  'password2',)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        # user.user_type = self.cleaned_data.get('user_type')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user', 'user_type',)

    def get_user_type(self, obj):
        user_type = obj.user.get_user_type_display()
        return user_type
