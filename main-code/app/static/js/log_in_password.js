// for customers' password log in
document.addEventListener('DOMContentLoaded', function () {
    const passwordLoginForm = document.getElementById('passwordLoginForm');

    if (passwordLoginForm) {
        passwordLoginForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(passwordLoginForm);
            const email = formData.get('email');
            const password = formData.get('password');

            fetch('/log_in_password', {
                method: 'POST',
                body: new URLSearchParams(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        alert(data.message);
                        window.location.href = '/';
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while processing your request.');
                });
        });
    }
});