from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UsersRegister, UsersMatchView, UsersView

router = SimpleRouter()
# router.register(r'clients', ClientViewSet)
urlpatterns = [
    # path('', api_root),
    path('auth/', include('rest_framework.urls')),
    path('clients/create/', UsersRegister.as_view({'post': 'create'})),
    path('clients/<int:id>/match/', UsersMatchView.as_view({'get': 'get', 'post': 'post'})),
    path('list/', UsersView.as_view({'get': 'list'}))
]
# urlpatterns += router.urls
