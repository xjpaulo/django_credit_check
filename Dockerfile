FROM python:3.9.6

WORKDIR /django-credit-check
COPY . /django-credit-check
RUN pip3 install -r requirements.txt
EXPOSE 8080