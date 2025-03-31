from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=50)
    customer_id = serializers.CharField(max_length=50)
    amount = serializers.FloatField()
    transaction_type = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    transaction_timestamp = serializers.DateTimeField()
    ip_address = serializers.IPAddressField()
    avg_spending = serializers.FloatField()
    avg_transaction_count = serializers.IntegerField()
    last_transaction_time = serializers.DateTimeField()
