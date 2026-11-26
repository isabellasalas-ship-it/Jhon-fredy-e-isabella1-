from rest_framework.routers import DefaultRouter

from camisetas.views import CamisetaViewSet, VentaViewSet

router = DefaultRouter()
router.register("camisetas", CamisetaViewSet, basename="camiseta")
router.register("ventas", VentaViewSet, basename="venta")

urlpatterns = router.urls