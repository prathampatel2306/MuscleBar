document.addEventListener('DOMContentLoaded', () => {
    // Micro-interactions for button press scaling
    const buttons = document.querySelectorAll('button');

    buttons.forEach(button => {
        button.addEventListener('mousedown', () => {
            button.classList.add('scale-95');
        });

        button.addEventListener('mouseup', () => {
            button.classList.remove('scale-95');
        });

        button.addEventListener('mouseleave', () => {
            button.classList.remove('scale-95');
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("workoutModal");
    const closeModalBtn = document.getElementById("closeWorkoutModal");
    const cancelBtn = document.getElementById("cancelWorkoutBtn");
    const addExerciseBtn = document.getElementById("addExerciseBtn");
    const exerciseRows = document.getElementById("exerciseRows");

    const requestIdInput = document.getElementById("workoutRequestId");
    const memberName = document.getElementById("workoutMemberName");

    const assignButtons = document.querySelectorAll(".assign-workout-btn");

    // Open modal
    assignButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const requestId = this.dataset.requestId;
            const name = this.dataset.memberName;

            requestIdInput.value = requestId;
            memberName.textContent = "For " + name;

            modal.classList.add("active");

        });

    });

    // Close modal
    function closeModal() {
        modal.classList.remove("active");
    }

    closeModalBtn.addEventListener("click", closeModal);

    cancelBtn.addEventListener("click", closeModal);

    // Close when clicking outside modal
    modal.addEventListener("click", function (event) {

        if (event.target === modal) {
            closeModal();
        }

    });

    // Add exercise
    addExerciseBtn.addEventListener("click", function () {

        const row = document.createElement("div");

        row.className = "exercise-row";

        row.innerHTML = `
    <input
        type="text"
        name="exercise[]"
        placeholder="Exercise"
        required>

    <input
        type="number"
        name="sets[]"
        placeholder="Sets"
        min="1"
        required>

    <input
        type="text"
        name="reps[]"
        placeholder="8-12"
        required>

    <button
        type="button"
        class="remove-exercise-btn">

        <span class="material-symbols-outlined">
            delete
        </span>

    </button>
`;

        exerciseRows.appendChild(row);

    });

    // Remove exercise
    exerciseRows.addEventListener("click", function (event) {

        const removeButton =
            event.target.closest(".remove-exercise-btn");

        if (!removeButton) {
            return;
        }

        const rows =
            exerciseRows.querySelectorAll(".exercise-row");

        // Keep at least one exercise row
        if (rows.length > 1) {
            removeButton.parentElement.remove();
        }

    });

});