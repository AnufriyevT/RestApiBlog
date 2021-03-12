from rest_framework import routers

from posts.views import NetworkViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'posts', NetworkViewSet)
router.register(r'users', UserViewSet)

urlpatterns = []
urlpatterns += router.urls