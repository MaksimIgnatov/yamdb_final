from django.utils import timezone
from rest_framework import serializers


def year_validate(value):
    year_now = timezone.now().year
    if year_now < value:
        raise serializers.ValidationError(
            'Год не может быть больше текущего!'
        )
    return value
