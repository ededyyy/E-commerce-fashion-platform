$(document).ready(function () {
    $('#add-product-form').on('submit', function (e) {
        e.preventDefault();

        // Prevent form submission if no category is selected
        var selectedCategories = $('input[name="category_ids[]"]:checked').length;
        if (selectedCategories === 0) {
            alert("Please select at least one category.");
            return;
        }

        var formData = new FormData(this);

        // Send ajax to backend
        $.ajax({
            url: '/add_product',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                alert(response.message);
                if (response.status === 'success') {
                    window.location.reload();
                }
            },
            error: function (xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });
});