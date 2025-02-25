document.addEventListener('DOMContentLoaded', function () {
    // Obtain modal forms
    const updatePersonalInfoForm = document.getElementById('updatePersonalInfoForm');
    const updateEmailForm = document.getElementById('updateEmailForm');
    const updatePasswordForm = document.getElementById('updatePasswordForm');
    const addAddressForm = document.getElementById('addAddressForm');
    const editAddressForm = document.getElementById('editAddressForm');
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

    // Personal information form
    if (updatePersonalInfoForm) {
        updatePersonalInfoForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(updatePersonalInfoForm);
            const username = formData.get('username');
            const firstname = formData.get('firstname');
            const lastname = formData.get('lastname');

            const currentUsername = updatePersonalInfoForm.dataset.username;
            const currentFirstname = updatePersonalInfoForm.dataset.firstname;
            const currentLastname = updatePersonalInfoForm.dataset.lastname;

            // Check if there are any changes
            if (username === currentUsername &&
                firstname === currentFirstname &&
                lastname === currentLastname) {
                alert('No changes made.');
                return;
            }

            fetch('/update_user', {
                method: 'POST',
                body: new URLSearchParams(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        alert(data.message);
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while updating your information.');
                });
        });
    }

    // Email form
    if (updateEmailForm) {
        const sendEmailCodeButton = document.getElementById('sendEmailCode');
        const emailCodeInput = document.getElementById('emailCode');

        // Send verification code
        if (sendEmailCodeButton) {
            sendEmailCodeButton.addEventListener('click', function () {
                const email = document.getElementById('email').value;

                const currentEmail = updateEmailForm.dataset.email;

                if (email === currentEmail) {
                    alert('No changes made.');
                    return;
                }

                fetch('/send_mail', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: email }),
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
            });
        }

        // Submit email form
        updateEmailForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(updateEmailForm);
            const email = formData.get('email');
            const code = formData.get('code');

            const currentEmail = updateEmailForm.dataset.email;

            if (email === currentEmail) {
                alert('No changes made.');
                return;
            }

            // Verify the code first
            fetch('/verify_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // If code is valid, submit the email change request
                        fetch('/update_email', {
                            method: 'POST',
                            body: new URLSearchParams(formData),
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === "success") {
                                    alert(data.message);
                                    window.location.reload();
                                } else {
                                    alert(data.message);
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                alert('An error occurred while updating your email.');
                            });
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while verifying the code.');
                });
        });
    }

    // Password form
    if (updatePasswordForm) {
        updatePasswordForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(updatePasswordForm);
            const currentPassword = formData.get('current_password');
            const newPassword = formData.get('new_password');
            const confirmNewPassword = formData.get('confirm_new_password');

            if (!passwordRegex.test(newPassword)) {
                alert('Invalid Password form.');
                return;
            }

            if (newPassword !== confirmNewPassword) {
                alert('New passwords do not match.');
                return;
            }

            if (newPassword === currentPassword) {
                alert('New password is the same as the current password.');
                return;
            }

            fetch('/update_password', {
                method: 'POST',
                body: new URLSearchParams(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        alert(data.message);
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while updating your password.');
                });
        });
    }

    // Add Address form
    if (addAddressForm) {
        addAddressForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(addAddressForm);

            fetch('/add_address', {
                method: 'POST',
                body: new URLSearchParams(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the address.');
                });
        });
    }

    // Edit Address form
    if (editAddressForm) {
        editAddressForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(editAddressForm);

            fetch('/update_address', {
                method: 'POST',
                body: new URLSearchParams(formData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while updating the address.');
                });
        });
    }

    // Delete Address
    window.deleteAddress = function (addressId) {
        if (confirm('Are you sure you want to delete this address?')) {
            fetch(`/delete_address/${addressId}`, {
                method: 'POST',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the address.');
                });
        }
    };

    // Set data for editing an address
    window.setEditAddressData = function (addressId) {
        fetch(`/api/address/${addressId}`)
            .then(response => response.json())
            .then(address => {
                document.getElementById('edit_address_id').value = address.id;
                document.getElementById('edit_country').value = address.country;
                document.getElementById('edit_province').value = address.province;
                document.getElementById('edit_city').value = address.city;
                document.getElementById('edit_street').value = address.street;
            })
            .catch(error => {
                console.error('Error fetching address:', error);
                alert('Failed to fetch address details.');
            });
    };
});