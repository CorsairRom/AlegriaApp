from rest_framework.routers import DefaultRouter
from ApiArriendosAlegria.views import TrabajadorViewSet, ComunaReadOnlyViewSet,TypeWorkerViewSet

router = DefaultRouter()

router.register(r'trabajador', TrabajadorViewSet, basename="trabajador")
router.register(r'comunas', ComunaReadOnlyViewSet, basename="comunas")
router.register(r'tipo_trabajador', TypeWorkerViewSet, basename="tipo_trabajador")

urlpatterns = router.urls