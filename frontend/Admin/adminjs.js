var app = angular.module('adminApp', []);
        app.controller('AdminController', function($scope, $http) {
            $scope.transactions = [];
            $scope.filteredTransactions = [];
            $scope.error = "";
            $scope.currentPage = 1;
            $scope.recordsPerPage = 10;
            
            var isAdmin = true;
            if (!isAdmin) {
                $scope.error = "Access Denied! Only Admins can view this page.";
                return;
            }

            $scope.filterTransactions = function() {
                if (!$scope.fromDate || !$scope.toDate) {
                    $scope.filteredTransactions = $scope.transactions;
                }
                var requestData = {
                    fromDate: $scope.fromDate,  // Make sure these match Django's expected field names
                    toDate: $scope.toDate
                };
        
                // Call backend API
                $http.post('http://127.0.0.1:8000/transaction/admin/', requestData)
                    .then(function(response) {
                        console.log("Filtered transactions:", response.data);
                        $scope.filteredTransactions = response.data;
                        $scope.currentPage = 1;
                        $scope.totalPages = Math.ceil($scope.filteredTransactions.length / $scope.recordsPerPage);
                    })
                    .catch(function(error) {
                        console.error("Error fetching transactions:", error);
                        $scope.error = "Failed to fetch transactions.";
                    });
                /*** else {
                    var from = new Date($scope.fromDate);
                    var to = new Date($scope.toDate);
                    $scope.filteredTransactions = $scope.transactions.filter(tx => {
                        var transactionDate = new Date(tx.date);
                        return transactionDate >= from && transactionDate <= to;
                    });
                }
                $scope.currentPage = 1;
                $scope.totalPages = Math.ceil($scope.filteredTransactions.length / $scope.recordsPerPage); ***/
            }; 
        });