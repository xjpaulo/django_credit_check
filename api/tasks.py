from celery import shared_task
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)


@shared_task
def validate_credit(user_age, credit_value):
    time.sleep(60)
    if user_age >= 18 and credit_value < 100000:
        logger.info(f'Age {user_age} is >= 18 and credit value {credit_value} is <= 100000.00')
        return 'Credit approved!'
    else:
        if user_age < 18:
            logger.info(f'Age {user_age} is < 18')
        if credit_value > 100000:
            logger.info(f'Credit value {credit_value} is > 100000')
        return 'Credit not approved.'
