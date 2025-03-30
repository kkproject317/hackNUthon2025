from django.db import models

class Transaction(models.Model):
    Transaction_id = models.IntegerField()
    Customer_id = models.CharField(max_length = 14)
    Customer_name = models.CharField(max_length =100)
    Amount = models.CharField(max_length =6)
    Transaction_type = models.CharField(max_length = 100)
    Location = models.CharField(max_length = 100)
    Transaction_Timestamp = models.DateTimeField()
    IP_Address = models.GenericIPAddressField()
    avg_spending = models.CharField(max_length = 6)
    avg_transaction_count = models.CharField(max_length = 100)
    Last_transaction_time = models.DateTimeField()
    # Behavioral_Flags = models.JSONField(default=list)  # Stores behavioral analysis flags
    # Rule_Based_Flags = models.JSONField(default=list)  # Stores rule-based fraud flags
    # Fraud_Score = models.FloatField(default=0.0)
