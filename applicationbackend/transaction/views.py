from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import transaction, Customer
from .serializers import transactionSerializers, inputSerializers, CustomerSerializer
from django.db.models import Avg, Max
from django.utils.timezone import now
from datetime import datetime, timedelta
import requests

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
        CustomerAvgSpending = transaction.objects.filter(customerId=customerId).aggregate(avg_amount=Avg('amount'))
        current_month = now().month
        current_year = now().year
        MonthlyAvgTransactions = (
            transaction.objects
            .filter(customerId=customerId, timeStamp__month=current_month, timeStamp__year=current_year)
            .aggregate(avg_transaction=Avg('amount'))
        )
        
        avgAmount = CustomerAvgSpending.get('avg_amount', 0)
        avgTransaction = MonthlyAvgTransactions.get('avg_transaction', 0)
        
        print(avgAmount,avgTransaction)
        
        fdsURL = "http://127.0.0.1:8001/detect/predict-fraud/"
        fdsPayload = {
            "transaction_id": 1,
            "customer_id": customerId,
            "amount":amount,
            "transaction_type":serializer.validated_data['transactionType'],
            "longitude":serializer.validated_data.get('longitude'),
            "latitude": serializer.validated_data.get('latitude'),
            "transaction_timestamp":now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip,
            "avg_spending":avgAmount,
            "avg_transaction_count":avgTransaction
        }
    
        fdsResponse = requests.post(fdsURL,fdsPayload)
        #print(fdsResponse)
        if fdsResponse.status_code == 200:
            fraud_data = fdsResponse.json()
            #print(fraud_data)
            fraudScore = fraud_data.get("fraud_prediction", 0)
        else:
            fraudScore = 0
            
        transaction_obj = transaction.objects.create(
            customerId = customerId,
            amount = amount,
            transactionType = serializer.validated_data['transactionType'],
            IP_address = ip if ip else None,  # Add IP Address
            latitude = serializer.validated_data.get('latitude'),
            longitude = serializer.validated_data.get('longitude'),
            transactionStatus = "Confirm", 
            fraudScore = fraudScore
        )
        
        return Response(transactionSerializers(transaction_obj).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin(request):
    fromDate = request.data.get('fromDate')
    toDate = request.data.get('toDate')
    if not fromDate or not toDate:
        return Response({"error":"Both from_Date and to_Date are required"},status=status.HTTP_400_BAD_REQUEST)
    
     # Convert string to datetime
     
    fd = fromDate[:fromDate.index('T')]
    td = toDate[:toDate.index('T')]
    from_date = datetime.strptime(fd, "%Y-%m-%d")
    print(from_date)
    # Set to_date to the END of the day (23:59:59) to include all transactions from that day
    to_date = datetime.strptime(td, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
    print(to_date)
    transactions = transaction.objects.filter(timeStamp__range=[from_date, to_date])
    return Response(transactionSerializers(transactions, many=True).data, status=status.HTTP_200_OK)