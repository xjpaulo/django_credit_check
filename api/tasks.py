from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded
import time


logger_celery = get_task_logger(__name__)


@shared_task(soft_time_limit=50, time_limit=60)
def validate_credit(user_age, credit_value):
    logger_celery.info(f'Validation task started: user_age: {user_age}, credit_value: {credit_value}')
    try:
        time.sleep(40)
        message_return = detailed_log = ''
        if user_age >= 18 and credit_value < 100000:
            detailed_log = f'Credit approved: Age {user_age} is >= 18 and credit value {credit_value} is < 100000.00'
            message_return = 'Credit approved: All values match the requirements.'
        elif user_age < 18:
            detailed_log = f'Credit not approved: Age {user_age} is < 18'
            message_return = 'Credit rejected: Minimum age allowed is 18.'
        elif credit_value >= 100000:
            detailed_log = f'Credit not approved: Credit value {credit_value} is >= 100000'
            message_return = 'Credit rejected: Maximum credit value allowed is 99999.'
        logger_celery.info(f'Validation task finished: {detailed_log}')
    except SoftTimeLimitExceeded:
        message_return = 'An error occurred when running the validation task.'
        logger_celery.warning(f'Validation task aborted due to SoftTimeLimitExceeded.')
    return message_return
