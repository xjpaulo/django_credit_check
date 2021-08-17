from rest_framework import serializers


class CreditCheckSerializer(serializers.Serializer):
    user_age = serializers.IntegerField(required=True)
    credit_value = serializers.FloatField(required=True)

