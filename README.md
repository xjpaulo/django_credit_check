# django-credit-check

A REST API responsible to perform credit validation based on age and credit amount provided. The API returns a ticket that could be accessed later to check whether the user is eligible for credit or not. It was developed using Python, Django Rest Framework, Celery and Redis.

## Summary

The API receives a payload containing the user's age and credit amount:
- Case the user's age is greater than or equal to 18, and the credit amount requested is less than 100000, then the credit should be approved.
- Case the user's age is less than 18, or the credit amount requested is greater than 100000, then the credit should be rejected.

A ticket will be returned when requesting credit validation. A task resposible for the validation will run in the background or be queued. The user can verify the status of the validation providing the ticket through one of the endpoints available.

## Requirements

 - [git](https://git-scm.com/)
 - [docker](https://docs.docker.com/)
 - [docker-compose](https://docs.docker.com/compose/)
 - [redis](https://redis.io/)

It's recommended to use some Linux distribution as OS.

## Configuration
To start the application, run docker-compose in the root directory:
```
$ sudo docker-compose up --detach --build
```
Logs can be followed by the command:  
```
$ sudo docker-compose logs --follow
```
## Operation
After the configuration, run the tests in order to check if everything is running fine:
```
$ sudo docker exec -it django_credit_check_web_1 python manage.py test
```

The API will be available through the endpoints below

**Endpoints:**

 - Credit check:
```
POST localhost:8080/api/v1/credit-check/

JSON Payload: {"user_age": <user_age>, "credit_value": <credit_value>}
```
 - Check results using a ticket:
``` 
GET localhost:8080/api/v1/credit-check/tickets/<ticket>/
```

**Tasks:**

Tasks can be monitored through Flower accessing the following URL:
```
http://localhost:5555
```
