from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
] + router.urls
