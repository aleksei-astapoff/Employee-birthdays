from django.core.exceptions import ValidationError


def validate_unique_subscription(model, user, birthday_person):
    if user == birthday_person:
        raise ValidationError('Нельзя подписаться на самого себя.')
    if model.objects.filter(
         user=user, birthday_person=birthday_person).exists():
        raise ValidationError('Подписка уже существует.')
