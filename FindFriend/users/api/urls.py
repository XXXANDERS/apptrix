from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import ClientsCreate

router = SimpleRouter()
# router.register(r'clients', ClientViewSet)
urlpatterns = [
    # path('', api_root),
    path('auth/', include('rest_framework.urls')),
    path('clients/create/', ClientsCreate.as_view({'post': 'create'}))
]
# urlpatterns += router.urls
