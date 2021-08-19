from django.urls import path
from .views import CreditCheck, Results
from . import views


urlpatterns = [
    path('credit-check/', CreditCheck.as_view(), name='credit_check'),
    path('credit-check/tickets/<str:ticket>/', Results.as_view(), name='results'),
    path('', views.api_root)
]