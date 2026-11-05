from rest_framework.routers import DefaultRouter

from camisetas.views import CamisetaViewSet

router = DefaultRouter()
router.register("camisetas", CamisetaViewSet, basename="camiseta")

urlpatterns = router.urls