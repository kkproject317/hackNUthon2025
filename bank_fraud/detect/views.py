import joblib
import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

# Load the model at startup
model_path = os.path.join(settings.BASE_DIR, "models/fraud_detection_model.pkl")
model = joblib.load(model_path)

class FraudDetectionView(APIView):
    def post(self, request):
        # Get transaction data from request
        transaction_data = request.data  # Assume it's a dictionary
        #print(transaction_data)
        if(transaction_data["transaction_type"] == "payment"):
            txn_type = 0
        elif(transaction_data["transaction_type"] == "withdraw"):
            txn_type = 1
        elif(transaction_data["transaction_type"] == "transfer"):
            txn_type = 2
        # Extract features in the same order as used for training
        features = [
            hash(transaction_data["transaction_id"]) % (10 ** 8),
            hash(transaction_data["customer_id"]) % (10 ** 8),
            transaction_data["amount"],
            txn_type,
            transaction_data["longitude"],
            transaction_data["latitude"],
            hash(str(transaction_data["transaction_timestamp"])) % (10 ** 8),
            #transaction_data["hour_of_day"],
            1,
            #transaction_data["day_of_week"],
            1,
            hash(transaction_data["ip_address"]) % (10 ** 8),
            transaction_data["avg_spending"],
            transaction_data["avg_transaction_count"]
        ]

        # # Predict fraud probability
        prediction = model.predict([features])[0]
        #print(prediction)
        return Response({"fraud_prediction": int(prediction)})


## ok so go ahead and do this tomorrow morning :-
# withdram, payment etc maate ek 0,1,2 nu mapping banav je
# time na label encoding maate kai sodh je ke kai rite int ma change thase?
# pehli bey columns ne kai rite int ma change karis?