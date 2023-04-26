from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ApiArriendosAlegria.api import user_api_view
from ApiArriendosAlegria.api import user_detail_api_view
from ApiArriendosAlegria.views import get_api_regions, get_api_banks, get_api_TypeAccountsBanks, get_post_api_CrudTyperWorkers,\
    get_put_delete_CrudTyperWorkers


urlpatterns = [
    path('usuario/', user_api_view, name='user_api_view'),
    path('usuario/<int:pk>/', user_detail_api_view, name='user_detail_api_view'),
    path('regiones/', get_api_regions, name='get_api_regions'),
    path('bancos/', get_api_banks, name='get_api_banks'),
    path('tipo_cuentas_bancos/', get_api_TypeAccountsBanks, name='get_api_TypeAccountsBanks'),
    path('tipo_trabajador/', get_post_api_CrudTyperWorkers, name='get_post_api_CrudTyperWorkers'),
    path('tipo_trabajador/<int:tpTrab_id>', get_put_delete_CrudTyperWorkers, name='get_put_delete_CrudTyperWorkers'),
    path('', include('ApiArriendosAlegria.routers'), name='trabjador_router'),
    
]
