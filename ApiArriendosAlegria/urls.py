from django.urls import path
from ApiArriendosAlegria.api import user_api_view
from ApiArriendosAlegria.api import user_detail_api_view


urlpatterns = [
    path('usuario/', user_api_view, name='user_api_view'),
    path('usuario/<int:pk>/', user_detail_api_view, name='user_detail_api_view'),
    
]
