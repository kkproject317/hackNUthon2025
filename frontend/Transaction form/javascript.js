// var app = angular.module('TransactionApp', []);

// app.controller('TransactionController', function($scope) {
//     $scope.customerID = "";
//     $scope.transactionAmount = "";
//     $scope.transactionType = "";

//     $scope.formatCustomerID = function() {
//         $scope.customerID = $scope.customerID.replace(/\D/g, '').slice(0, 12);
//         $scope.customerID = $scope.customerID.replace(/(\d{4})(?=\d)/g, '$1-');
//     };

//     $scope.validateForm = function() {
//         var customerIDPattern = /^\d{4}-\d{4}-\d{4}$/;
//         if (!$scope.customerID.match(customerIDPattern) || $scope.customerID.length !== 14) {
//             alert("Invalid Customer ID. It should be exactly 14 characters in XXXX-XXXX-XXXX format.");
//             return false;
//         }

//         if ($scope.transactionAmount > 1000000.00){
//             alert("Transcation limit reached.")
//             return false;
//         }


//         alert("Transaction successful!");
//     //     $scope.transactiondata = {
//     //         customerId: $scope.customer.customerId,
//     //         amount: $scope.customer.amount,
//     //         transactionType: $scope.customer.transactionType,
//     //         latitude:null,
//     //         longitude:null
//     //     }
//     //     navigator.geolocation.getCurrentPosition(
//     //         function(position) {
//     //             // Update latitude and longitude
//     //             $scope.transactiondata.latitude = position.coords.latitude;
//     //             $scope.transactiondata.longitude = position.coords.longitude;
//     //             $scope.$apply();  // Ensure changes reflect in AngularJS scope
    
//     //             // Send data to backend
//     //             $http.post('/api/transaction/', $scope.transactiondata)
//     //                 .then(function(response) {
//     //                     console.log("Transaction successful:", response.data);
//     //                 })
//     //                 .catch(function(error) {
//     //                     console.error("Error:", error);
//     //                 });
//     //         },
//     //         function(error) {
//     //             console.error("Error getting location:", error);
    
//     //             // Still send transaction if location is unavailable
//     //             $http.post('/api/transaction/', $scope.transactiondata)
//     //                 .then(function(response) {
//     //                     console.log("Transaction successful (without location):", response.data);
//     //                 })
//     //                 .catch(function(error) {
//     //                     console.error("Error:", error);
//     //                 });
//     //         }
//     //     );
//     };
    

    
// });



var app = angular.module('TransactionApp', []);

        app.controller('TransactionController', function($scope) {
            $scope.customer = {
                customerID: "",
                amount: null,
                transactionType: ""
            };

            $scope.errors = {};

            // Function to format Customer ID
            $scope.formatCustomerID = function() {
                let rawID = $scope.customer.customerID.replace(/\D/g, '').slice(0, 12);
                let formattedID = rawID.replace(/(\d{4})(?=\d)/g, '$1-');

                // Ensure proper formatting in input field
                $scope.customer.customerID = formattedID;
            };

            // Form validation function
            $scope.validateForm = function(event) {
                event.preventDefault(); // Prevent page refresh
                $scope.errors = {}; // Clear previous errors

                var customerIDPattern = /^\d{4}-\d{4}-\d{4}$/;

                // Validate Customer ID
                if (!$scope.customer.customerID.match(customerIDPattern)) {
                    $scope.errors.customerID = "Invalid format! Use XXXX-XXXX-XXXX.";
                }

                // Validate Transaction Amount
                if ($scope.customer.amount === null || $scope.customer.amount <= 0) {
                    $scope.errors.amount = "Please enter a valid amount.";
                } else if ($scope.customer.amount > 1000000) {
                    $scope.errors.amount = "Transaction limit exceeded (Max: 1,000,000).";
                }

                // Validate Transaction Type
                if (!$scope.customer.transactionType) {
                    $scope.errors.transactionType = "Please select a transaction type.";
                }

                // If no errors, show success message
                if (Object.keys($scope.errors).length === 0) {
                    alert("Transaction successful!");
                }
            };
        });