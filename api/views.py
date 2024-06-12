
from django.db.models.expressions import Value
from django.db.models import BooleanField
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User, Subscribe
from api.serializers import (CustomUserSerializer, SubscriptionsSerializer,
                             SubscribeSerializer)


class UserViewSet(UserViewSet):
    """ ViewSet для работы с пользователями. """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),)
    def subscriptions(self, request):

        user = request.user
        queryset = User.objects.filter(
            following__user=user
        ).annotate(is_subscribed=Value(True, output_field=BooleanField())
                   ).order_by('following__user')

        serializer = SubscriptionsSerializer(
            queryset, many=True,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        birthday_person = get_object_or_404(User, id=id)
        data = {
            'user': request.user.id,
            'birthday_person': birthday_person.id
        }

        serializer = SubscribeSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True, )
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        subscription = Subscribe.objects.filter(
            user=request.user,
            birthday_person_id=id
        )
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Подписка не найдена'},
                        status=status.HTTP_404_NOT_FOUND)
