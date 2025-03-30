var app = angular.module('TransactionApp', []);

app.controller('TransactionController', function($scope) {
    $scope.customerID = "";
    $scope.transactionAmount = "";
    $scope.transactionType = "";

    $scope.formatCustomerID = function() {
        $scope.customerID = $scope.customerID.replace(/\D/g, '').slice(0, 12);
        $scope.customerID = $scope.customerID.replace(/(\d{4})(?=\d)/g, '$1-');
    };

    $scope.validateForm = function() {
        var customerIDPattern = /^\d{4}-\d{4}-\d{4}$/;
        if (!$scope.customerID.match(customerIDPattern) || $scope.customerID.length !== 14) {
            alert("Invalid Customer ID. It should be exactly 14 characters in XXXX-XXXX-XXXX format.");
            return false;
        }

        if ($scope.transactionAmount > 1000000.00){
            alert("Transcation limit reached.")
            return false;
        }


        alert("Transaction successful!");
    //     $scope.transactiondata = {
    //         customerId: $scope.customer.customerId,
    //         amount: $scope.customer.amount,
    //         transactionType: $scope.customer.transactionType,
    //         latitude:null,
    //         longitude:null
    //     }
    //     navigator.geolocation.getCurrentPosition(
    //         function(position) {
    //             // Update latitude and longitude
    //             $scope.transactiondata.latitude = position.coords.latitude;
    //             $scope.transactiondata.longitude = position.coords.longitude;
    //             $scope.$apply();  // Ensure changes reflect in AngularJS scope
    
    //             // Send data to backend
    //             $http.post('/api/transaction/', $scope.transactiondata)
    //                 .then(function(response) {
    //                     console.log("Transaction successful:", response.data);
    //                 })
    //                 .catch(function(error) {
    //                     console.error("Error:", error);
    //                 });
    //         },
    //         function(error) {
    //             console.error("Error getting location:", error);
    
    //             // Still send transaction if location is unavailable
    //             $http.post('/api/transaction/', $scope.transactiondata)
    //                 .then(function(response) {
    //                     console.log("Transaction successful (without location):", response.data);
    //                 })
    //                 .catch(function(error) {
    //                     console.error("Error:", error);
    //                 });
    //         }
    //     );
    };
    

    
});