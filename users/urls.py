from django.urls import path
from rest_framework.routers import DefaultRouter

# from .views import UserViewSets
from .views import UserViewSets

router = DefaultRouter()
router.register(r'', UserViewSets, basename='users')
app_name = 'user'
urlpatterns = router.urls
# urlpatterns += [
#
# ]
