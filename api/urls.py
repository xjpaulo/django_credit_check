from django.urls import path
from .views import CreditCheck, Results


urlpatterns = [
    path('credit_check/', CreditCheck.as_view(), name='credit check'),
    path('results/<str:ticket>/', Results.as_view(), name='results'),
]
