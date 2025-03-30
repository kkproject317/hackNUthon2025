from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import transaction, Customer
from .serializers import transactionSerializers, inputSerializers, CustomerSerializer
from django.db.models import Avg
from django.db.models.functions import Cast

@api_view(['POST'])
def transactions(request):
    serializer = inputSerializers(data = request.data)
    if serializer.is_valid():
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        customerId = serializer.validated_data['customerId']
        amount = serializer.validated_data['amount']
        
        try:
            customer = Customer.objects.get(customerId = customerId)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found"},status=status.HTTP_404_NOT_FOUND)
        
        if customer.balance < amount:
            return Response({"Error":"Insuffiecient Funds"},status=status.HTTP_400_BAD_REQUEST)
        
        customer.balance -= amount
        customer.save()
        CustomerAvgSpending = transaction.objects.filter(customerId=customerId).aaggregate(Avg('amount'))
        MonthlyAvgTransactions = 
    
        #call fds api 
        
        #get response from api for fraud score and set it 
        
        
        #now save to transaction
        transaction_obj = transaction.objects.create(
            customerId = customerId,
            amount = amount,
            transactionType = serializer.validated_data['transactionType'],
            IP_address = ip,  # Add IP Address
            latitude = serializer.validated_data.get('latitude'),
            longitude = serializer.validated_data.get('longitude'),
            transactionStatus = "Confirm", 
            fraudScore = 0  # Placeholder
        )
        
        
        return Response(transactionSerializers(transaction_obj).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#transaction report (from date to date)