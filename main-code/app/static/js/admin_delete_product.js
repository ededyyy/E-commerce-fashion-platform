// can delete products
$(document).ready(function () {
    $('.delete-btn').on('click', function (event) {
        event.preventDefault();

        var productId = $(this).data('product-id');

        if (confirm('Delete this product?')) {
            $.ajax({
                url: '/delete_product/' + productId,
                type: 'DELETE',
                success: function (response) {
                    if (response.status === 'success') {
                        window.location.href = response.redirect_url;
                    } else {
                        alert(response.message);
                    }
                },
                error: function (xhr, status, error) {
                    alert('An error occurred: ' + error);
                }
            });
        }
    });
});
