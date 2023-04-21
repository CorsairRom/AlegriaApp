from rest_framework.routers import DefaultRouter
from ApiArriendosAlegria.views import TrabajadorViewSet, ComunaReadOnlyViewSet

router = DefaultRouter()

router.register(r'trabajador', TrabajadorViewSet, basename="trabajador")
router.register(r'comunas', ComunaReadOnlyViewSet, basename="comunas")

urlpatterns = router.urls