from celery import shared_task
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)


@shared_task
def validate_credit(user_age, credit_value):
    time.sleep(60)
    message_return = message_log = ''
    if user_age >= 18 and credit_value < 100000:
        message_log = f'Credit approved: Age {user_age} is >= 18 and credit value {credit_value} is <= 100000.00'
        message_return = 'Credit approved: All values match the requirements.'
    elif user_age < 18:
        message_log = f'Credit not approved: Age {user_age} is < 18'
        message_return = 'Credit not approved: Minimum age allowed is 18.'
    elif credit_value > 100000:
        message_log = f'Credit not approved: Credit value {credit_value} is > 100000'
        message_return = 'Credit not approved: Maximum credit value allowed is 100000.'
    logger.info(message_log)
    return message_return
