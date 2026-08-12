document.addEventListener('DOMContentLoaded', () => {
    // Isolated UI interactive triggers
    const logoutBtn = document.querySelector('.logout-btn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            // Add custom logout logic or backend redirection here
            window.location.href = '/login';
        });
    }
});

// Standard function to switch screen state if needed dynamically
function showState(state) {
    const assigned = document.getElementById('state-assigned');
    const unassigned = document.getElementById('state-unassigned');

    if (!assigned || !unassigned) return;

    if (state === 'assigned') {
        assigned.classList.remove('hidden');
        unassigned.classList.add('hidden');
    } else {
        assigned.classList.add('hidden');
        unassigned.classList.remove('hidden');
    }
}