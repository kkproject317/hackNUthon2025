from django.urls import path
from .views import receive_transaction

urlpatterns = [
    path('', receive_transaction, name='receive_transaction'),
]
