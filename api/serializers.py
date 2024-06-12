from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для пользователя. """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'date_of_birth',
            'first_name',
            'last_name',
            'department',
            'is_subscribed'
        )
        read_only_fields = (
            'id',
            'email',
            'date_of_birth',
            'first_name',
            'last_name',
            'department',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.follower.filter(birthday_person=obj).exists())


class SubscriptionsSerializer(CustomUserSerializer):
    """ Сериализатор для подписки. """

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields


class SubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор для подписки. """

    class Meta:
        model = Subscribe
        fields = '__all__'

    def validate(self, data):
        if data['user'] == data['birthday_person']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        if Subscribe.objects.filter(
            user=data['user'],
            birthday_person=data['birthday_person']
        ).exists():
            raise serializers.ValidationError(
                'Подписка уже существует.'
            )
        return data

    def to_representation(self, instance):
        return SubscriptionsSerializer(
            instance.birthday_person, context=self.context).data
