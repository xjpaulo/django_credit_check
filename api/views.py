from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreditCheckSerializer
from .tasks import validate_credit
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request):
    return Response({'error': 'Please use a valid endpoint.'}, status=status.HTTP_404_NOT_FOUND)


class CreditCheck(APIView):
    def post(self, request):
        logger.debug(f'Received POST request: {request.data}')
        serializer = CreditCheckSerializer(data=request.data)

        if serializer.is_valid():
            validation_queue = validate_credit.delay(serializer.validated_data['user_age'],
                                                     serializer.validated_data['credit_value'])
            logger.debug(f'Task for validation created. Ticket id: {validation_queue.id}')
            return Response({'ticket_id': validation_queue.id})
        logger.error(f'Error when serializing: {serializer.errors}')
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Results(APIView):
    def get(self, request, ticket):
        logger.debug(f'Received GET request for ticket {ticket}')
        result = AsyncResult(str(ticket))
        if result.status == 'SUCCESS':
            response = Response({
                'ticket_id': ticket,
                'ticket_status': result.status,
                'result': result.get()
            }, status=status.HTTP_200_OK)
            result.revoke(terminate=True)
            logger.debug(f'Returned message for ticket {ticket}: {result.get()}')
        elif result.status == 'PENDING':
            response = Response({
                'ticket_id': ticket,
                'ticket_status': result.status,
                'result': 'The credit check task is enqueued or ticket does not exist.'
            }, status=status.HTTP_200_OK)
            logger.debug(f'Returned message for ticket {ticket}:'
                         f'The credit check task is enqueued or ticket does not exist.')
        elif result.status == 'STARTED':
            response = Response({
                'ticket_id': ticket,
                'ticket_status': result.status,
                'result': 'The credit is being checked right now, please try again in a few seconds.'
            }, status=status.HTTP_200_OK)
            logger.debug(f'Returned message for ticket {ticket}:'
                         f'The credit is being checked right now, please try again in a few seconds.')
        elif result.status == 'FAILURE':
            response = Response({
                'ticket_id': ticket,
                'ticket_status': result.status,
                'result': 'There was a failure in the credit check.'
            })
            logger.debug(f'Returned message for ticket {ticket}: There was a failure in the credit check.')
        else:
            response = Response({
                'status': result.status,
                'ticket_id': ticket,
            })
            logger.debug(f'Returned message for ticket {ticket}: {result.state}')
        return response


