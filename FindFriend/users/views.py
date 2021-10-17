from decimal import Decimal

from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from users.geo import get_distance
from users.api.serializers import UsersCreateSerializer, UsersMatchSerializer, UsersMatchCreateSerializer, \
    UsersSerializer
from users.models import CustomUser, UserMatch


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'profile': reverse('profile', request=request, format=format),
        'clients': reverse('clients-list', request=request, format=format),
    })


class Profile(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersCreate(mixins.CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersCreateSerializer


class UsersView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.filter(is_staff=False, is_active=True).all()
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'sex']
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        d = request.query_params.get('distance')
        if d:
            if not d.replace('.', '', 1).isdigit() or len(d) > 9:
                return Response({"distance": ["Выберите корректный вариант. "
                                              "Дистанция должна быть действительным числом не более 9 символов."]})
            self.queryset = self.users_nearby_filter(request.query_params.get('distance'), queryset=self.queryset)
        return self.list(request, *args, **kwargs)

    def users_nearby_filter(self, distance, queryset):
        distance = Decimal(distance)
        user = self.request.user
        users = queryset.filter(~Q(longitude=None), ~Q(latitude=None)).values('id', 'latitude', 'longitude')
        users_id = []
        for u in users:
            d = get_distance(user.latitude, user.longitude, u['latitude'], u['longitude'])
            if d < distance:
                users_id.append(u['id'])
        users2 = CustomUser.objects.filter(id__in=users_id)
        data = []
        return users2


class UsersMatchView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    queryset = UserMatch.objects.select_related('from_user', 'for_user')
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.match = None
        self.for_user = None
        super(UsersMatchView, self).__init__()

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
        self.for_user = CustomUser.objects.filter(id=self.kwargs['id']).first()
        self.match = UserMatch.objects.filter(from_user=self.request.user, for_user=self.kwargs['id']).first()
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['from_user'] = self.request.user
        serializer.validated_data['for_user'] = self.for_user
        serializer.save()

    def create(self, request, *args, **kwargs):
        if self.for_user == self.request.user:
            return Response({'detail': 'добавление связи между одним пользователем невозможна'},
                            status=status.HTTP_400_BAD_REQUEST)
        if self.match:
            return Response({'detail': 'связь уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.for_user:
            return Response({'detail': 'пользователь не найден'}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        if response_data.get('like'):
            user1 = CustomUser.objects.get(id=response_data.get('from_user'))
            user2 = CustomUser.objects.get(id=response_data.get('for_user'))
            match2 = UserMatch.objects.filter(from_user=response_data.get('for_user'),
                                              for_user=response_data.get('from_user')).first()
            if match2 and match2.like:
                response_data[
                    'info'] = f'У вас взаимная симпатия с {user2.first_name} {user2.last_name}, почта = {user2.email}'

                # отправка почты  (нужно настроить конфиг на сервере)
                subject = 'FindFriend response'
                try:
                    send_mail(
                        subject,
                        f'«Вы понравились {user1.first_name} {user1.last_name}! '
                        f'Почта участника: {user1.email}»',
                        from_email=None, recipient_list=[f'{user2.email}']
                    )
                    send_mail(
                        subject,
                        f'«Вы понравились {user2.first_name} {user2.last_name}! '
                        f'Почта участника: {user2.email}»',
                        from_email=None, recipient_list=[f'{user1.email}']
                    )
                except BadHeaderError as e:
                    print('Errors:', e)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UsersDistance(GenericViewSet):
    def get(self, request, *args, **kwargs):
        user1 = CustomUser.objects.filter(id=self.kwargs['id1']).first()
        user2 = CustomUser.objects.filter(id=self.kwargs['id2']).first()
        if user1 and user2:
            if user1.latitude and user1.longitude and user2.latitude and user2.longitude:
                # вычисляем расстояние между пользователями
                d = get_distance(user1.latitude, user1.longitude, user2.latitude, user2.longitude)
                return Response({'data': f'Расстояние равно {d} км'})
            return Response(f'У пользователя отсутствуют гео-даные')
        return Response(f'Пользователя(ей) не существует')
