document.addEventListener('DOMContentLoaded', () => {
    // Focus micro-interactions for input wrapper labels
    const inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            const group = input.closest('.input-group');
            if(group) {
                const label = group.querySelector('.input-label');
                if(label) label.style.color = 'var(--primary)';
            }
        });
        input.addEventListener('blur', () => {
            const group = input.closest('.input-group');
            if(group) {
                const label = group.querySelector('.input-label');
                if(label) label.style.color = 'var(--on-surface-variant)';
            }
        });
    });

    // Handle Form Submission & Trigger Popup Modal
    const form = document.getElementById('trainerProfileForm');
    const modal = document.getElementById('completeModal');
    const closeBtn = document.getElementById('modalCloseBtn');

    if (form) {
    form.addEventListener('submit', () => {
        // Allow the browser to submit the form normally
    });
    }

    // Close Modal / Proceed Action
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            // Optional: Uncomment below if you want to clear/submit the form afterwards
            // form.submit();
        });
    }
});