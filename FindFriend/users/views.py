from django.shortcuts import render
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.api.serializers import ClientsCreateSerializer
from users.models import CustomUser


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'clients': reverse('customuser-list', request=request, format=format),
#     })


class ClientsCreate(mixins.CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ClientsCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientsView(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ClientsCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# class ClientViewSet(ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = ClientsSerializer
#
#     def get_serializer_class(self):
#         if self.request.method in ['GET', 'OPTIONS', 'HEAD', 'PUT', 'PATCH']:
#             return ClientsSerializer
#         elif self.request.method in ['POST']:
#             return ClientsCreateSerializer
#
#
# def get(self, request, *args, **kwargs):
#     return self.retrieve(request, *args, **kwargs)
#
#
# def post(self, request, *args, **kwargs):
#     return self.create(request, *args, **kwargs)
