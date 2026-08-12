document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("profileForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {

        const fullName = document.querySelector('[name="full_name"]').value.trim();
        const dob = document.querySelector('[name="date_of_birth"]').value;
        const gender = document.querySelector('[name="gender"]').value;
        const height = document.querySelector('[name="height"]').value;
        const weight = document.querySelector('[name="weight"]').value;
        const experience = document.querySelector('input[name="experience_level"]:checked');

        if (
            fullName === "" ||
            dob === "" ||
            gender === "" ||
            height === "" ||
            weight === "" ||
            !experience
        ) {
            e.preventDefault();
            alert("Please complete all fields before continuing.");
            return;
        }

        if (parseFloat(height) <= 0 || parseFloat(weight) <= 0) {
            e.preventDefault();
            alert("Height and Weight must be greater than 0.");
            return;
        }

        // IMPORTANT:
        // Do NOT call e.preventDefault() here.
        // Let the browser submit the form to Flask.
    });

});