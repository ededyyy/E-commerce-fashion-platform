document.addEventListener('DOMContentLoaded', function () {  // function for admin log in
    const signInAdminForm = document.getElementById('signInAdminForm');

    signInAdminForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(signInAdminForm);

        fetch('/sign_in_admin', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = '/admin_product_management';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request.');
            });
    });
});