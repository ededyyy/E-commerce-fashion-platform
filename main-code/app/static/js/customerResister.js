document.addEventListener('DOMContentLoaded', function () {
    // Obtain the form elements
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const emailInput = document.getElementById('email');
    const getCodeButton = document.getElementById('getCode');
    const verificationSection = document.getElementById('verificationSection');
    const verificationCodeInput = document.getElementById('verificationCode');
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

    // Confirm the password
    function validatePassword() {
        const password = passwordInput.value;
        if (!passwordRegex.test(password)) {
            alert('Invalid Password form.');
            return false;
        }
        return true;
    }

    // Check if the two inputs of passwords are the same
    function validateConfirmPassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return false;
        }
        return true;
    }

    // Confirm the validation of email
    function validateEmail() {
        const email = emailInput.value;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            return false;
        }
        return true;
    }

    // Real-time Verification of Password
    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const password = passwordInput.value;
            if (!passwordRegex.test(password)) {
                passwordInput.style.borderColor = 'red';
                passwordInput.focus();
            } else {
                passwordInput.style.borderColor = 'green';
            }
        });
    }

    // Real-time Verification of Password and Confirm Password
    if (passwordInput && confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function () {
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            if (password !== confirmPassword) {
                confirmPasswordInput.style.borderColor = 'red';
                confirmPasswordInput.focus();
            } else {
                confirmPasswordInput.style.borderColor = 'green';
            }
        });
    }

    // When click the get code button
    if (getCodeButton) {
        getCodeButton.addEventListener('click', function () {
            if (!validateEmail()) {
                return;
            }

            fetch('/check_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: emailInput.value, action: "register" }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        alert('This email is already registered. Please use a different email.');
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
                                    verificationSection.style.display = 'block';
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

    // Handle the registration form submission
    function handleRegister(event) {
        event.preventDefault();

        if (!validatePassword() || !validateConfirmPassword() || !validateEmail()) {
            return;
        }

        const userEnteredCode = verificationCodeInput.value;

        // Verify the code before submitting the registration form
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
                    // If the code is valid, proceed with registration
                    submitRegistration();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while verifying the code.');
            });
    }

    // Submit the registration form
    function submitRegistration() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const firstname = document.getElementById('firstname').value;
        const lastname = document.getElementById('lastname').value;
        const email = document.getElementById('email').value;

        fetch('/Register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                firstname: firstname,
                lastname: lastname,
                email: email,
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
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
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});