/**
 * The Muscle Bar - Membership Path Selector Logic
 */

document.addEventListener("DOMContentLoaded", function () {

    // Modal Elements
    const paymentModal = document.getElementById("paymentModal");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const modalAmountField = document.getElementById("modalAmountField");
    const modalTierName = document.getElementById("modalTierName");
    const dummyPayBtn = document.getElementById("dummyPayBtn");

    // Plan Selection Buttons
    const selectButtons = document.querySelectorAll(".select-btn");

    // Stores the selected membership plan
    let selectedPlan = "";

    // Open Payment Modal
    selectButtons.forEach(button => {

        button.addEventListener("click", function (event) {

            const chosenAmount = event.target.getAttribute("data-amount");
            const chosenTier = event.target.getAttribute("data-tier");

            // Save selected plan
            selectedPlan = chosenTier;

            // Update Modal Content
            modalAmountField.textContent = chosenAmount;
            modalTierName.textContent = chosenTier;

            // Show Modal
            paymentModal.classList.remove("hidden");
        });

    });

    // Close Modal (X Button)
    closeModalBtn.addEventListener("click", function () {
        paymentModal.classList.add("hidden");
    });

    // Close Modal (Click Outside)
    window.addEventListener("click", function (event) {

        if (event.target === paymentModal) {
            paymentModal.classList.add("hidden");
        }

    });

    // Complete Transaction
    dummyPayBtn.addEventListener("click", function () {

        paymentModal.classList.add("hidden");

        // Create a hidden form
        const form = document.createElement("form");

        form.method = "POST";
        form.action = "/plan";

        // Hidden input for selected plan
        const input = document.createElement("input");

        input.type = "hidden";
        input.name = "plan";
        input.value = selectedPlan;

        form.appendChild(input);

        document.body.appendChild(form);

        // Submit to Flask
        form.submit();

    });

});
