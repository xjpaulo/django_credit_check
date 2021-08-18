from celery import shared_task
from celery.utils.log import get_task_logger
import time
import logging

logger = logging.getLogger(__name__)
logger_celery = get_task_logger(__name__)


@shared_task
def validate_credit(user_age, credit_value):
    logger.debug('Validation task started.')
    time.sleep(60)
    message_return = message_log = ''
    if user_age >= 18 and credit_value < 100000:
        message_log = f'Credit approved: Age {user_age} is >= 18 and credit value {credit_value} is <= 100000.00'
        message_return = 'Credit approved: All values match the requirements.'
    elif user_age < 18:
        message_log = f'Credit not approved: Age {user_age} is < 18'
        message_return = 'Credit rejected: Minimum age allowed is 18.'
    elif credit_value > 100000:
        message_log = f'Credit not approved: Credit value {credit_value} is > 100000'
        message_return = 'Credit rejected: Maximum credit value allowed is 100000.'
    logger.debug(f'Validation task finished: {message_log}')
    logger_celery.info(message_log)
    return message_return
