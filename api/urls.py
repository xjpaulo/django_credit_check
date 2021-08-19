from django.urls import path
from .views import CreditCheck, Results
from . import views


urlpatterns = [
    path('api/v1/credit-check/', CreditCheck.as_view(), name='credit_check'),
    path('api/v1/credit-check/tickets/<str:ticket>/', Results.as_view(), name='results'),
    path('', views.api_root)
]