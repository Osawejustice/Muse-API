from rest_framework import viewsets

from users.serializers import UserSerializer
from .models import User


class UserViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


