// For check product details, add to cart
let currentProductId = null;

document.addEventListener('DOMContentLoaded', function () {
    const cartToast = document.getElementById('cartToast');
    if (cartToast) {
        const toast = new bootstrap.Toast(cartToast, {
            autohide: true,
            delay: 1000
        });
    }

    const modalAddToCartBtn = document.getElementById('modalAddToCartBtn');
    if (modalAddToCartBtn) {
        modalAddToCartBtn.addEventListener('click', function (event) {
            handleAddToCart(event, null);
        });
    }
});

// Handle with click the img
function handleImageClick(event, productId) {
    event.stopPropagation();
    currentProductId = productId;

    fetch(`/api/products/${productId}`)
        .then(response => response.json())
        .then(product => {
            document.getElementById('modalProductImage').src = product.img_url;
            document.getElementById('modalProductName').textContent = product.name;
            document.getElementById('modalProductDescription').textContent = product.description;
            document.getElementById('modalProductPrice').textContent = '¥' + product.price.toLocaleString();

            const modal = new bootstrap.Modal(document.getElementById('productModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching product details:', error);
        });
}

function handleAddToCart(event, productId) {
    event.stopPropagation();

    const targetProductId = productId || currentProductId;
    if (!targetProductId) return;

    // Fetch the current stock of the product
    fetch(`/api/product/stock/${targetProductId}`)
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
            const stock = parseInt(stockData.stock, 10);

            // Fetch the current quantity of the product in the cart
            fetch('/api/cart/items')
                .then(response => {
                    if (response.status === 401) {
                        alert('Please log in first.');
                        return Promise.reject('Unauthorized');
                    }
                    if (!response.ok) {
                        throw new Error('Failed to fetch cart items');
                    }
                    return response.json();
                })
                .then(cartItems => {
                    // Find the current quantity of the product in the cart
                    const cartItem = cartItems.find(item => item.product_id === targetProductId);
                    const currentQuantityInCart = cartItem ? cartItem.quantity : 0;
                    console.log('Current Quantity in Cart:', currentQuantityInCart);

                    // Check if adding one more item would exceed the stock
                    if (currentQuantityInCart + 1 > stock) {
                        alert('Cannot add more items. Quantity exceeds stock.');
                        return; // Stop further execution
                    }

                    // Add the product to the cart
                    fetch('/api/cart/add', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ productId: targetProductId })
                    })
                        .then(response => {
                            if (response.status === 401) {
                                alert('Please log in first.');
                                return;
                            }
                            return response.json();
                        })
                        .then(data => {
                            if (data && data.success) {
                                sessionStorage.setItem('showCartToast', 'true');
                                window.location.reload();
                            } else if (data) {
                                alert('Fail to add product to cart.');
                            }
                        })
                        .catch(error => {
                            console.error('Error adding to cart:', error);
                            alert('Fail to add product to cart.');
                        });
                })
                .catch(error => {
                    if (error !== 'Unauthorized') {
                        console.error('Error fetching cart items:', error);
                        alert('Failed to fetch cart items. Please try again.');
                    }
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

document.addEventListener('DOMContentLoaded', function () {
    if (sessionStorage.getItem('showCartToast') === 'true') {
        const cartToast = document.getElementById('cartToast');
        if (cartToast) {
            const toast = new bootstrap.Toast(cartToast);
            toast.show();
        }

        sessionStorage.removeItem('showCartToast');
    }
});