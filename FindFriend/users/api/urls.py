from django.urls import path, include

from users.views import UsersView, UsersCreate, UsersMatchView, UsersDistance, api_root

urlpatterns = [
    path('', api_root),
    path('auth/', include('rest_framework.urls')),
    path('clients/create/', UsersCreate.as_view({'post': 'create'}), name='register'),
    path('clients/<int:id>/', UsersView.as_view({'get': 'retrieve'})),
    path('list/', UsersView.as_view({'get': 'get'}), name='clients-list'),
    path('clients/<int:id>/match/', UsersMatchView.as_view({'get': 'get', 'post': 'post'})),

    # нужно ли?
    path('clients/distance/<int:id1>/<int:id2>/', UsersDistance.as_view({'get': 'get'})),

]
