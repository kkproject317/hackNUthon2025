

var app = angular.module('TransactionApp', []);

        app.controller('TransactionController', function($scope,$http) {
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

                console.log(navigator)
                if(navigator.geolocation){
                    navigator.geolocation.getCurrentPosition(
                        function(position){
                            latitude = position.coords.latitude,
                            longitude = position.coords.longitude
                            // Update CustomerData inside the callback
                            $scope.$apply(() => {
                                $scope.CustomerData = {
                                    customerId: $scope.customer.customerID,
                                    amount: $scope.customer.amount,
                                    transactionType: $scope.customer.transactionType,
                                    latitude: latitude,
                                    longitude: longitude
                                };
                            });
                            $http.post('http://127.0.0.1:8000/transaction/user/',$scope.CustomerData)
                            .then(function (response) {
                                // Success callback
                                console.log("Transaction successful:", response.data);
                            })
                            .catch(function (error) {
                                // Error callback
                                console.error("Error in transaction:", error);
                            });
                            // If no errors, show success message
                            alert("Transaction successful!");        
                        },
                        function (error) {
                            console.error("Error getting location:", error.message);
                        }
                    );
                }else{
                    console.error("Geolocation is not supported by this browser.")
                }
            };
        });