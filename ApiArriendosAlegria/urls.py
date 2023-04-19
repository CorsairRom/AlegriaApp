from django.urls import path
from ApiArriendosAlegria.api import user_api_view
from ApiArriendosAlegria.api import user_detail_api_view
from ApiArriendosAlegria.views import get_api_regions, get_api_comunas_by_id_reg, get_api_banks, get_api_TypeAccountsBanks, get_post_api_CrudTyperWorkers


urlpatterns = [
    path('usuario/', user_api_view, name='user_api_view'),
    path('usuario/<int:pk>/', user_detail_api_view, name='user_detail_api_view'),
    path('regiones/', get_api_regions, name='get_api_regions'),
    path('comunas/<int:id_reg>/', get_api_comunas_by_id_reg, name='get_api_comunas_by_id_reg'),
    path('bancos/', get_api_banks, name='get_api_banks'),
    path('tipo_cuentas_bancos/', get_api_TypeAccountsBanks, name='get_api_TypeAccountsBanks'),
    path('tipo_trabajador/', get_post_api_CrudTyperWorkers, name='get_post_api_CrudTyperWorkers'),
    
]
