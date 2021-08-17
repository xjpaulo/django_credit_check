from rest_framework import serializers


class CreditCheckSerializer(serializers.Serializer):
    user_age = serializers.IntegerField(required=True, min_value=18)
    credit_value = serializers.FloatField(required=True, max_value=100000.00)

