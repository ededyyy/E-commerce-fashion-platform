// Pay function
function payOrder(orderId) {
    fetch(`/pay_order/${orderId}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Payment successful!');
                window.location.href = '/order';
            } else {
                alert(data.message || 'Payment failed.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your payment.');
        });
}

// Remove order function
function removeOrder(orderId) {
    if (confirm('Are you sure you want to remove this order?')) {
        fetch(`/remove_order/${orderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to remove order: ' + data.message);
                }
            });
    }
}

// Refund and return function
function refundAndReturn(orderId) {
    if (confirm('Request a refund and return?')) {
        fetch(`/refund_and_return/${orderId}`, {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

// Confirm receipt
function confirmReceipt(orderId) {
    if (confirm('Are you sure you have received the order?')) {
        fetch(`/confirm-receipt/${orderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to confirm receipt.');
                }
            });
    }
}

// Filter by status
document.addEventListener('DOMContentLoaded', function () {
    const statusElement = document.getElementById('status');
    if (statusElement) {
        statusElement.addEventListener('change', function () {
            this.form.submit();
        });
    }
});