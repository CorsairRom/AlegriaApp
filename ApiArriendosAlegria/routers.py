from rest_framework.routers import DefaultRouter
from ApiArriendosAlegria.views import TrabajadorViewSet, ComunaReadOnlyViewSet,TypeWorkerViewSet, PropietarioViewSet, PropiedadViewSet, CuentaViewSet, ArriendatarioViewSet,\
                                        ArriendoViewSet, PersonalidadJuridicaViewSet, TipoPropiedadViewSet, DetalleArriendoViewSet, ServiciosExtrasViewSet, GastoComunViewSet,\
                                        UsuarioViewSet

router = DefaultRouter()

router.register(r'usuario', UsuarioViewSet, basename="usuario")
router.register(r'trabajador', TrabajadorViewSet, basename="trabajador")
router.register(r'comunas', ComunaReadOnlyViewSet, basename="comunas")
router.register(r'tipo_trabajador', TypeWorkerViewSet, basename="tipo_trabajador")
router.register(r'propietario', PropietarioViewSet, basename="propietario")
router.register(r'cuenta', CuentaViewSet, basename="cuenta")
router.register(r'personalidad_juridica', PersonalidadJuridicaViewSet, basename="personalidad_juridica")
router.register(r'propiedad', PropiedadViewSet, basename="propiedad")
router.register(r'tipo_propiedad', TipoPropiedadViewSet, basename="tipo_propiedad")
router.register(r'arrendatario', ArriendatarioViewSet, basename="arrendatario")
router.register(r'arriendo', ArriendoViewSet, basename="arriendo")
router.register(r'detalle_arriendo', DetalleArriendoViewSet, basename="detalle_arriendo")
router.register(r'servicios_extras', ServiciosExtrasViewSet, basename="servicios_extras")
router.register(r'gasto_comun', GastoComunViewSet, basename="gasto_comun")

urlpatterns = router.urls
