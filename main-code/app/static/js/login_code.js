document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('emailCode');
    const verificationCodeInput = document.getElementById('verificationCode');
    const verificationSection = document.getElementById('verificationSection');
    const sendVerificationCodeButton = document.getElementById('sendVerificationCode');
    const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

    // Validate email
    function validateEmail() {
        const email = emailInput.value;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            return false;
        }
        return true;
    }

    // Send verification code
    if (sendVerificationCodeButton) {
        sendVerificationCodeButton.addEventListener('click', function () {
            if (!validateEmail()) {
                return;
            }

            fetch('/check_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: emailInput.value, action: "login" }),
            })
                .then(response => response.json())
                .then(data => {
                    if (!data.exists) {
                        alert('This email is not registered. Please register first.');
                    } else {
                        fetch('/send_mail', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ email: emailInput.value }),
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    alert(data.message);
                                } else {
                                    alert(data.message);
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('An error occurred while sending the verification code.');
                            });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while checking the email.');
                });
        });
    }

    // Handle form submission for login with code
    const verificationLoginForm = document.getElementById('verificationLoginForm');
    if (verificationLoginForm) {
        verificationLoginForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const userEnteredCode = verificationCodeInput.value;

            // Verify the code before submitting the login request
            fetch('/verify_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: userEnteredCode }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // If the code is valid, proceed with login
                        const formData = new FormData(this);
                        fetch('/login_with_code', {
                            method: 'POST',
                            body: new URLSearchParams(formData),
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === "success") {
                                    alert(data.message);
                                    window.location.href = '/'; // Redirect to home page
                                } else {
                                    alert(data.message);
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('An error occurred while processing your request.');
                            });
                    } else {
                        alert(data.message); // If code is invalid, show error message
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while verifying the code.');
                });
        });
    }
});