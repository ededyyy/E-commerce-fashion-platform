// Function for editing products
$(document).ready(function () {
    $('form[id^="editProductForm"]').on('submit', function (e) {
        e.preventDefault();

        var formId = $(this).attr('id');
        var formData = new FormData(this);

        // Prevent form submission if no category is selected
        var selectedCategories = $(this).find('input[name="category_ids[]"]:checked').length;
        if (selectedCategories === 0) {
            alert('Please select at least one category.');
            return;
        }

        $.ajax({
            url: '/edit_product/' + formId.split('editProductForm')[1],
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.status === 'success') {
                    window.location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr, status, error) {
                alert('An error occurred: ' + error);
            }
        });
    });
});
