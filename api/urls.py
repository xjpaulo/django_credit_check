from django.urls import path
from .views import CreditCheck, Results


urlpatterns = [
    path('credit/', CreditCheck.as_view(), name='credit_check'),
    path('results/<str:ticket>/', Results.as_view(), name='results'),
]
