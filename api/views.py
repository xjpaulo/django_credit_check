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
            return Response({'ticket_id': validation_queue.id})
        return Response({'errors': serializer.errors})


class Results(APIView):
    def get(self, request, ticket, *args, **kwargs):
        result = AsyncResult(str(ticket))
        if result.status == 'SUCCESS':
            response = Response({
                'ticket_id': ticket,
                'result': result.get()
            }, status=status.HTTP_200_OK)
            result.revoke(terminate=True)
        elif result.status == 'PENDING':
            response = Response({
                'ticket_id': ticket,
                'result': 'The credit check is enqueued, please try again later.'
            }, status=status.HTTP_200_OK)
        elif result.status == 'STARTED':
            response = Response({
                'ticket_id': ticket,
                'result': 'The credit is being checked right now, please try again in a few seconds.'
            }, status=status.HTTP_200_OK)
        else:
            response = Response({
                'status': result.state,
                'ticket_id': ticket,
            })
        return response
