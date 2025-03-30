from .models import transaction, Customer
from rest_framework import serializers

class transactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = transaction
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class inputSerializers(serializers.Serializer):
    customerId = serializers.CharField(max_length=12)
    amount = serializers.DecimalField(max_digits=9,decimal_places=2)
    transactionType = serializers.CharField(max_length=9)
    IP_address = serializers.IPAddressField(allow_null=True, required=False)
    latitude = serializers.DecimalField(max_digits=9,decimal_places=6,allow_null=True,required=False)
    longitude = serializers.DecimalField(max_digits=9,decimal_places=6,allow_null=True,required=False)
    