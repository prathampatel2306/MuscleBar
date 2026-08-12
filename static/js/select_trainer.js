document.addEventListener('DOMContentLoaded', () => {
    const selectButtons = document.querySelectorAll('.select-btn');
    const modal = document.getElementById('trainerModal');
    const selectedTrainerSpan = document.getElementById('selectedTrainerName');
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Attach click events to all trainer selection buttons
    selectButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const trainerName = e.target.getAttribute('data-trainer');

            // Set dynamic trainer name inside modal text
            if (selectedTrainerSpan) {
                selectedTrainerSpan.textContent = trainerName;
            }

            // Display the modal popup
            if (modal) {
                modal.classList.remove('hidden');
            }
        });
    });

    // Close modal when confirmation action is pressed
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            if (modal) {
                modal.classList.add('hidden');
            }
        });
    }

    // Close modal if user clicks outside the modal box
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
});