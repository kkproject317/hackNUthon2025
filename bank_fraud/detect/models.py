from django.db import models

class transaction_data(models.Model):
    transaction_id = models.CharField(max_length=50, primary_key=True)  # Unique identifier
    customer_id = models.CharField(max_length=14)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    transaction_timestamp = models.DateTimeField()
    hour_of_day = models.IntegerField()
    day_of_week = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    avg_spending = models.FloatField()
    avg_transaction_count = models.IntegerField()
    last_transaction_time = models.DateTimeField()
    fraud_score = models.FloatField(null=True, blank=True)
    fraud_label = models.CharField(max_length=20, null=True, blank=True)
