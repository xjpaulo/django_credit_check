from celery import shared_task, Celery


@shared_task
def validate_credit(user_age, credit_value):
    if user_age > 18 and credit_value < 100000:
        return 'Credit approved!'
    else:
        return 'Credit not approved.'
