from django.urls import path
from .views import FraudDetectionView  

urlpatterns = [
    path('predict-fraud/', FraudDetectionView.as_view(), name='predict-fraud'),  
]
