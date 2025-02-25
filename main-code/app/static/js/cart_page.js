// Save the state of checkboxes to localStorage
function saveCheckboxState() {
    const checkedItems = [];
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        checkedItems.push(checkbox.id);
    });
    localStorage.setItem('checkedItems', JSON.stringify(checkedItems));
}

// Restore the state of checkboxes from localStorage
function restoreCheckboxState() {
    const checkedItems = JSON.parse(localStorage.getItem('checkedItems')) || [];
    checkedItems.forEach(id => {
        const checkbox = document.getElementById(id);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    updateTotalPrice();
}

// Restore checkbox state when the page loads
document.addEventListener('DOMContentLoaded', function () {
    restoreCheckboxState();

    document.querySelectorAll('.item-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            saveCheckboxState();
            updateTotalPrice();
        });
    });
});

// Update the quantity of a product in the cart
function updateQuantity(itemId, change, newValue) {
    const quantityInput = document.querySelector(`#quantityInput${itemId}`);
    const minusBtn = quantityInput.parentElement.querySelector('.minus-btn');
    let quantity = newValue || (parseInt(quantityInput.value) + change);
    if (quantity < 1) quantity = 1;
    // Fetch the current stock of the product
    fetch(`/api/product/stock/${itemId}`)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Product not found');
                } else {
                    throw new Error('Failed to fetch stock');
                }
            }
            return response.json();
        })
        .then(stockData => {
            const stock = stockData.stock;

            if (quantity > stock) {
                alert('Cannot add more items. Quantity exceeds stock.');
                quantity = stock;
            }

            quantityInput.value = quantity;
            minusBtn.disabled = quantity === 1;

            // Send the updated quantity to the server
            fetch(`/api/cart/update/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: quantity })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to update quantity');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.success) {
                        saveCheckboxState();
                        window.location.reload();
                    } else {
                        alert('Failed to update quantity.');
                    }
                })
                .catch(error => {
                    console.error('Error updating quantity:', error);
                    alert('Failed to update quantity. Please try again.');
                });
        })
        .catch(error => {
            console.error('Error fetching stock:', error);
            if (error.message === 'Product not found') {
                alert('Product not found. Please refresh the page.');
            } else {
                alert('Failed to check product stock. Please try again.');
            }
        });
}

// Remove a product from the cart
function removeItem(itemId) {
    fetch(`/api/cart/remove/${itemId}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            if (data && data.success) {
                saveCheckboxState();
                window.location.reload();
            } else {
                alert('Failed to remove item.');
            }
        })
        .catch(error => {
            console.error('Error removing item:', error);
            alert('Failed to remove item.');
        });
}

// Update the total price
function updateTotalPrice() {
    const totalPriceElement = document.getElementById('totalPrice');
    if (!totalPriceElement) {
        return;
    }

    let total = 0;
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        total += parseFloat(checkbox.getAttribute('data-price'));
    });
    totalPriceElement.textContent = `¥${total.toLocaleString()}`;
}

document.addEventListener('DOMContentLoaded', function () {
    updateTotalPrice();

    document.querySelectorAll('.item-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateTotalPrice);
    });
});

// Continue to check out function
function checkout() {
    // For address modal
    const addressModal = new bootstrap.Modal(document.getElementById('addressModal'));
    addressModal.show();
}

function proceedToCheckout() {
    const selectedAddress = document.querySelector('input[name="address"]:checked');
    if (!selectedAddress) {
        alert('Please select an address.');
        return;
    }

    const addressId = selectedAddress.value;

    const selectedItems = [];
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        const itemId = checkbox.id.replace('itemCheckbox', '');
        const quantity = document.getElementById(`quantityInput${itemId}`).value;
        selectedItems.push({ id: itemId, quantity: quantity });
    });

    if (selectedItems.length === 0) {
        alert('Please select at least one item to proceed to checkout.');
        return;
    }

    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items: selectedItems, address_id: addressId }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/order';
            } else {
                alert(data.message || 'Failed to proceed to checkout.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
}

function addAddress() {
    if (confirm('You have no addresses. Would you like to add one?')) {
        window.location.href = '/account';
    } else {
        const addressModal = bootstrap.Modal.getInstance(document.getElementById('addressModal'));
        addressModal.hide();
    }
}