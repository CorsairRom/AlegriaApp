from django.urls import path, include

urlpatterns = [
    path('', include('ApiArriendosAlegria.routers'), name='api_router'),
]
