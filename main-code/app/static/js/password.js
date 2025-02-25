// function to show and hide password
document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.querySelectorAll('.toggle-password');
    passwordInput.forEach(icon => {
        icon.addEventListener('click', function () {
            const label = this.closest('label');
            if (!label) {
                console.error('No <label> found for toggle icon');
                return;
            }
            const inputId = label.getAttribute('for');
            const input = document.getElementById(inputId);
            if (!input) {
                console.error(`No <input> found with id "${inputId}"`);
                return;
            }

            // show and hide of password
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            }
        });
    });
});