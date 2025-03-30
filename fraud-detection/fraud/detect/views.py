from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
import time
from datetime import datetime

# Mock storage for tracking recent transactions by IP
recent_transactions = {}

# AI Agent 1: Behavioral Analysis
def behavioral_analysis(transaction):
    """Analyze transaction behavior based on customer's history."""
    amount = float(transaction['Amount'])
    avg_spending = float(transaction['avg_spending'])
    last_txn_time = transaction['Last_transaction_time']
    risk_factors = []

    # Check if amount is significantly higher than usual
    if amount > 2.5 * avg_spending:
        risk_factors.append("High Spending Deviation")

    # Check if the transaction is happening at an unusual time
    try:
        txn_datetime = datetime.fromisoformat(last_txn_time)  # Convert to datetime
        hour = txn_datetime.hour  # Extract hour
        if hour < 5 or hour > 23:
            risk_factors.append("Unusual Transaction Timing")
    except ValueError:
        risk_factors.append("Invalid Transaction Time Format")

    return risk_factors


# AI Agent 2: Rule-Based Fraud Detection
def rule_based_fraud_detection(transaction):
    """Apply rule-based fraud checks."""
    amount = float(transaction['Amount'])
    txn_type = transaction['Transaction_type']
    ip_address = transaction['IP_Address']
    location = transaction['Location']
    timestamp = time.time()
    risk_factors = []

    # Large transaction alert
    if amount > 100000:
        risk_factors.append("High-Value Transaction")

    # Multiple transactions from the same IP within 1 minute
    if ip_address in recent_transactions:
        last_txn_time = recent_transactions[ip_address]
        if timestamp - last_txn_time < 60:
            risk_factors.append("Multiple Quick Transactions from Same IP Address")

    # Suspicious transaction from a new location
    recent_user_txns = Transaction.objects.filter(Customer_id=transaction['Customer_id']).order_by('-Transaction_Timestamp')[:5]
    known_locations = {txn.Location for txn in recent_user_txns}
    if location not in known_locations:
        risk_factors.append("Transaction from Unusual Location")

    # Large withdrawal alert
    if txn_type == "Cash Withdrawal" and amount > 50000:
        risk_factors.append("High Cash Withdrawal")

    # Store current transaction timestamp
    recent_transactions[ip_address] = timestamp

    return risk_factors


# Function to calculate fraud score from AI agents
def calculate_fraud_score(behavior_flags, rule_flags):
    """Generate fraud score based on AI agent flags."""
    base_score = 0
    if "High Spending Deviation" in behavior_flags:
        base_score += 30
    if "Unusual Transaction Timing" in behavior_flags:
        base_score += 20
    if "High-Value Transaction" in rule_flags:
        base_score += 40
    if "Multiple Quick Transactions from Same IP Address" in rule_flags:
        base_score += 25
    if "Transaction from Unusual Location" in rule_flags:
        base_score += 35
    if "High Cash Withdrawal" in rule_flags:
        base_score += 20

    return min(base_score, 100)  # Fraud score should not exceed 100


@api_view(['POST'])
def receive_transaction(request):
    """Django API endpoint to process transactions and save results in MySQL."""
    try:
        transaction = request.data  # Transaction dictionary
        print(transaction)

        # Run AI agents
        # behavior_flags = behavioral_analysis(transaction)
        # rule_flags = rule_based_fraud_detection(transaction)

        # Compute fraud score
        # fraud_score = calculate_fraud_score(behavior_flags, rule_flags)
        fraud_score = 1
        # Save transaction + AI results to MySQL
        transaction_obj = Transaction.objects.create(
            Transaction_id=transaction['Transaction_id'],
            Customer_id=transaction['Customer_id'],
            Amount=transaction['Amount'],
            Transaction_type=transaction['Transaction_type'],
            Location=transaction['Location'],
            Transaction_Timestamp=transaction['Transaction_Timestamp'],
            IP_Address=transaction['IP_Address'],
            avg_spending=transaction['avg_spending'],
            avg_transaction_count=transaction['avg_transaction_count'],
            Last_transaction_time=transaction['Last_transaction_time'],
            # Behavioral_Flags=behavior_flags,
            # Rule_Based_Flags=rule_flags,
            # Fraud_Score=fraud_score
        )

        # Send response
        response = {
            "Transaction ID": transaction['Transaction_id'],
            "Behavioral Flags": 1,
            "Rule-Based Flags": 2,
            "Fraud Score": fraud_score
        }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# # Mock storage for tracking recent transactions by IP and location
# recent_transactions = {}
# print(recent_transactions)

# # AI Agent 1: Behavioral Analysis
# def behavioral_analysis(transaction):
#     """Analyze transaction behavior based on customer's transaction history."""
#     customer_id = transaction['Customer_id']
#     amount = float(transaction['Amount'])
#     avg_spending = float(transaction['avg_spending'])
#     txn_time_str = transaction['Transaction_Timestamp']  # Fix: Use Transaction_Timestamp
#     risk_factors = []

#     # Check if amount is significantly higher than usual
#     if amount > 2.5 * avg_spending:
#         risk_factors.append("High Spending Deviation")

#     # Check if the transaction is happening at an unusual time
#     try:
#         print(f"Received datetime string: {txn_time_str}")  # Debugging step
#         txn_datetime = datetime.fromisoformat(txn_time_str)  # Convert to datetime object
#         hour = txn_datetime.hour  # Extract the hour
#         print(f"Extracted hour: {hour}")  # Debugging step

#         if hour < 5 or hour > 23:
#             risk_factors.append("Unusual Transaction Timing")
#     except ValueError:
#         risk_factors.append("Invalid Transaction Time Format")

#     return risk_factors


# # AI Agent 2: Rule-Based Fraud Detection
# def rule_based_fraud_detection(transaction):
#     """Apply rule-based fraud checks."""
#     txn_id = transaction['Transaction_id']
#     amount = float(transaction['Amount'])
#     txn_type = transaction['Transaction_type']
#     ip_address = transaction['IP_Address']
#     location = transaction['Location']
#     timestamp = time.time()
#     risk_factors = []

#     # Large transaction alert
#     if amount > 100000:
#         risk_factors.append("High-Value Transaction")

#     # Multiple transactions from same IP within 1 min
#     if ip_address in recent_transactions:
#         last_txn_time = recent_transactions[ip_address]
#         if timestamp - last_txn_time < 60:
#             risk_factors.append("Multiple Quick Transactions from Same IP Address")

#     # Suspicious transaction from a new location
#     recent_user_txns = Transaction.objects.filter(Customer_id=transaction['Customer_id']).order_by('-Transaction_Timestamp')[:5]
#     known_locations = {txn.Location for txn in recent_user_txns}
#     print(f"Known Locations for Customer {transaction['Customer_id']}: {known_locations}")
#     print(f"Current Transaction Location: {location}")
#     if len(known_locations) > 0 and location not in known_locations:
#         risk_factors.append("Transaction from Unusual Location")

#     # Large withdrawal alert
#     if txn_type == "Cash Withdrawal" and amount > 50000:
#         risk_factors.append("High Cash Withdrawal")

#     # Store current transaction timestamp
#     recent_transactions[ip_address] = timestamp

#     return risk_factors

# @api_view(['POST'])
# def receive_transaction(request):
#     """Django API endpoint to analyze transactions using AI agents."""
#     transaction = request.data  # transaction is a dictionary
#     print(transaction)
#     serializer = TransactionSerializer(data=request.data)
#     # if serializer.is_valid():
#     #     serializer.save()
#     # Call AI agent functions
#     behavior_flags = behavioral_analysis(transaction)
#     rule_flags = rule_based_fraud_detection(transaction)

#     response = {
#         "Transaction ID": transaction['Transaction_id'],
#         "Behavioral Flags": behavior_flags,
#         "Rule-Based Flags": rule_flags
#     }
    
#     return Response(response, status=status.HTTP_200_OK)



# # @api_view(['POST'])
# # def receive_transaction(request):
# #     serializer = TransactionSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response({"message": "Transaction received!", "data": serializer.data}, status=status.HTTP_201_CREATED)
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
