function formatCustomerID(input) {
    // Remove all non-digit characters
    let value = input.value.replace(/\D/g, '');
    
    // Format as XXXX-XXXX-XXXX (limit to 12 digits)
    if (value.length > 12) {
        value = value.slice(0, 12);
    }

    // Insert hyphens every 4 characters
    input.value = value.replace(/(\d{4})(?=\d)/g, '$1-');
}


function validateTransactionAmount(input) {
    input.value = input.value.replace(/\D/g, '').slice(0, 6);
}

function validateForm() {
    let customerID = document.getElementById("customerID").value.trim();
    let transactionAmount = document.getElementById("transactionAmount").value.trim();
    let transactionType = document.getElementById("transactionType").value;

    let customerIDPattern = /^\d{4}-\d{4}-\d{4}$/;
    if (!customerIDPattern.test(customerID) || customerID.length !== 14) {
        alert("Invalid Customer ID. It should be exactly 14 characters in XXXX-XXXX-XXXX format.");
        return false;
    }

    if (!/^[0-9]{1,6}$/.test(transactionAmount)) {
        alert("Invalid Transaction Amount. Enter up to 6 digits.");
        return false;
    }

    if (!transactionType) {
        alert("Please select a transaction type.");
        return false;
    }

    alert("Transaction successful!");
    return true;
}
