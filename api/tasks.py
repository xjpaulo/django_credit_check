from celery import shared_task
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)


@shared_task
def validate_credit(user_age, credit_value):
    time.sleep(60)
    if user_age >= 18 and credit_value < 100000:
        message = f'Credit approved: Age {user_age} is >= 18 and credit value {credit_value} is <= 100000.00'
    elif user_age < 18:
        message = f'Credit not approved: Age {user_age} is < 18'
    elif credit_value > 100000:
        message = f'Credit not approved: Credit value {credit_value} is > 100000'
    logger.info(message)
    return message
