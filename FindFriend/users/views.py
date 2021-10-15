from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.api.serializers import UsersCreateSerializer, UsersMatchSerializer, UsersMatchCreateSerializer, \
    UsersSerializer
from users.models import CustomUser, UserMatch


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'clients': reverse('customuser-list', request=request, format=format),
#     })


class UsersRegister(mixins.CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersCreateSerializer


# class Profile(mixins.RetrieveModelMixin, GenericViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UsersSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user


class UsersView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.filter(is_staff=False, is_active=True).all()
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'sex']
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user




class UsersMatchView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = UserMatch.objects.select_related('from_user', 'for_user')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return UsersMatchCreateSerializer
        return UsersMatchSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, from_user=self.request.user, for_user=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['from_user'] = self.request.user
        serializer.validated_data['for_user'] = CustomUser.objects.filter(id=self.kwargs['id']).first()
        serializer.save()

    def create(self, request, *args, **kwargs):
        # for_user = CustomUser.objects.filter(id=self.kwargs['id']).first()
        if not CustomUser.objects.filter(id=self.kwargs['id']).exists():
            return Response('Пользователь не существует')
        # request.data._mutable = True
        # request.data['for_user'] = CustomUser.objects.filter(id=self.kwargs['id']).first().id
        # request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
