document.addEventListener('DOMContentLoaded', function () {

    // 1. Password Visibility Logic for Both Input Buttons
    const passwordContainers = document.querySelectorAll('.password-input-container');

    passwordContainers.forEach(function (container) {
        const toggleBtn = container.querySelector('.toggle-password-btn');
        const inputField = container.querySelector('.password-field');

        if (toggleBtn && inputField) {
            toggleBtn.addEventListener('click', function () {
                const icon = this.querySelector('span');

                if (inputField.type === 'password') {
                    inputField.type = 'text';
                    icon.textContent = 'visibility_off';
                } else {
                    inputField.type = 'password';
                    icon.textContent = 'visibility';
                }
            });
        }
    });

    // 2. Real-time Password & Confirm Password Validation
    const passwordInput = document.getElementById('password');
    const passwordHint = document.getElementById('passwordHint');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const confirmPasswordHint = document.getElementById('confirmPasswordHint');

    // Function to check main password complexity
    function validatePasswordComplexity() {
        const value = passwordInput.value;

        if (value === "") {
            passwordHint.classList.add('hidden');
            return false;
        }

        const hasLetter = /[a-zA-Z]/.test(value);
        const hasNumber = /[0-9]/.test(value);
        const hasSymbol = /[^a-zA-Z0-9]/.test(value);

        if (hasLetter && hasNumber && hasSymbol) {
            passwordHint.classList.add('hidden');
            passwordInput.classList.remove('input-error');
            return true;
        } else {
            passwordHint.classList.remove('hidden');
            passwordInput.classList.add('input-error');
            return false;
        }
    }

    // Function to check if passwords match
    function validatePasswordMatch() {
        const passwordValue = passwordInput.value;
        const confirmValue = confirmPasswordInput.value;

        // If confirm field is empty, don't show the error yet
        if (confirmValue === "") {
            confirmPasswordHint.classList.add('hidden');
            return false;
        }

        if (passwordValue === confirmValue) {
            confirmPasswordHint.classList.add('hidden');
            confirmPasswordInput.classList.remove('input-error');
            return true;
        } else {
            confirmPasswordHint.classList.remove('hidden');
            confirmPasswordInput.classList.add('input-error');
            return false;
        }
    }

    // Run verification dynamically on input event triggers
    if (passwordInput && passwordHint) {
        passwordInput.addEventListener('input', function() {
            validatePasswordComplexity();
            // Re-validate match case if they modify the original password afterward
            if (confirmPasswordInput.value !== "") {
                validatePasswordMatch();
            }
        });
    }

    if (confirmPasswordInput && confirmPasswordHint) {
        confirmPasswordInput.addEventListener('input', validatePasswordMatch);
    }

    // 3. Signup Form Submission Management
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            // Check validation status before proceeding
            const isComplex = validatePasswordComplexity();
            const isMatching = validatePasswordMatch();

            if (!isComplex || !isMatching) {
                event.preventDefault(); // Stop submission if errors exist
                console.log("Form submission blocked due to validation errors.");
            } else {
                console.log("Form submission processed through custom script.");
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

    const adminRadio = document.getElementById("role-admin");
    const memberRadio = document.getElementById("role-member");
    const trainerRadio = document.getElementById("role-trainer");

    const adminCodeGroup = document.getElementById("adminCodeGroup");
    const adminCode = document.getElementById("adminCode");

    function toggleAdminCode() {
        if (adminRadio.checked) {
            adminCodeGroup.style.display = "block";
        } else {
            adminCodeGroup.style.display = "none";
            adminCode.value = "";
        }
    }

    adminRadio.addEventListener("change", toggleAdminCode);
    memberRadio.addEventListener("change", toggleAdminCode);
    trainerRadio.addEventListener("change", toggleAdminCode);

    // Run once when the page loads
    toggleAdminCode();

});