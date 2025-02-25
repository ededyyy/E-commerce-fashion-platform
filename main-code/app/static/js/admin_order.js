document.addEventListener('DOMContentLoaded', function () {
    // Ship order function
    function shipOrder(orderId) {
        fetch(`/ship-order/${orderId}`, {
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
                    alert('Failed to ship order.');
                }
            });
    }

    // Accept refund and return function
    function processRefund(orderId, acceptRefund) {
        fetch(`/process_refund/${orderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                accept_refund: acceptRefund
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to process refund: ' + data.message);
                }
            });
    }

    let currentOrderId = null;

    // For reject refund modal
    const rejectReasonModal = document.getElementById('rejectReasonModal');
    if (rejectReasonModal) {
        rejectReasonModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            currentOrderId = button.getAttribute('data-order-id');
        });
    }

    // For reject refund submission
    const submitRejectReasonButton = document.getElementById('submitRejectReason');
    if (submitRejectReasonButton) {
        submitRejectReasonButton.addEventListener('click', function () {
            const rejectReason = document.getElementById('rejectReason').value;

            if (!rejectReason) {
                alert('Please enter a reject reason.');
                return;
            }

            rejectRefund(currentOrderId, rejectReason);

            const modal = bootstrap.Modal.getInstance(document.getElementById('rejectReasonModal'));
            modal.hide();
        });
    }

    // Reject refund function
    function rejectRefund(orderId, rejectReason) {
        fetch(`/process_refund/${orderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                accept_refund: false,
                reject_reason: rejectReason
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Refund rejected successfully');
                    location.reload();
                } else {
                    alert('Failed to reject refund: ' + data.message);
                }
            });
    }

    // Expose functions to global scope if needed
    window.shipOrder = shipOrder;
    window.processRefund = processRefund;
    window.rejectRefund = rejectRefund;
});