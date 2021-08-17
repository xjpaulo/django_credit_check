from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreditCheckSerializer
from .tasks import validate_credit


class CreditCheck(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreditCheckSerializer(data=request.data)

        if serializer.is_valid():
            validation_queue = validate_credit.delay(serializer.validated_data['user_age'],
                                                     serializer.validated_data['credit_value'])
            return Response({'task_id': validation_queue.id})
        return Response({'errors': serializer.errors})


class Results(APIView):
    def get(self, request, token, *args, **kwargs):
        result = AsyncResult(str(token))
        if result.state == 'SUCCESS':
            response = Response({
                'status': result.state,
                'task_id': token,
                'result': result.get()
            }, status=status.HTTP_200_OK)
            result.revoke(terminate=True)
        else:
            response = Response({
                'status': result.state,
                'task_id': token,
            })
        return response
