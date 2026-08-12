document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('notice-form');
    const button = document.getElementById('broadcast-btn');
    const textarea = document.getElementById('notice-textarea');

    if (!form) return;

    form.addEventListener('submit', function (e) {

        if (textarea.value.trim() === '') {

            e.preventDefault();

            textarea.style.borderColor = 'var(--error)';

            setTimeout(() => {
                textarea.style.borderColor = 'var(--outline-variant)';
            }, 1000);

            return;
        }

        button.innerText = 'Broadcasting...';
        button.disabled = true;
        button.style.opacity = '0.7';
    });

});

document.getElementById("view-all-members").addEventListener("click", function () {

    document.querySelectorAll(".extra-member").forEach(function (row) {
        row.style.display = "table-row";
    });

    this.style.display = "none";
});

const viewAllTrainers = document.getElementById("view-all-trainers");

if (viewAllTrainers) {
    viewAllTrainers.addEventListener("click", function () {

        document.querySelectorAll(".extra-trainer").forEach(function (row) {
            row.style.display = "table-row";
        });

        this.style.display = "none";
    });
}

document.querySelectorAll(".member-age").forEach(function (cell) {

    const dob = cell.dataset.dob;

    if (!dob) {
        cell.textContent = "N/A";
        return;
    }

    const birthDate = new Date(dob);
    const today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();

    const monthDifference =
        today.getMonth() - birthDate.getMonth();

    if (
        monthDifference < 0 ||
        (
            monthDifference === 0 &&
            today.getDate() < birthDate.getDate()
        )
    ) {
        age--;
    }

    cell.textContent = age;
});

document.addEventListener("DOMContentLoaded", function () {

    const modal =
        document.getElementById("deleteMemberModal");

    const noBtn =
        document.getElementById("deleteNoBtn");

    const yesBtn =
        document.getElementById("deleteYesBtn");

    let formToDelete = null;


    /* ================================
       DELETE MEMBER
    ================================= */

    document.addEventListener("submit", function (event) {

        const form =
            event.target.closest(".delete-member-form");

        if (!form) {
            return;
        }

        event.preventDefault();
        event.stopPropagation();

        formToDelete = form;

        modal.classList.add("show");

    });


    /* ================================
       NO
    ================================= */

    noBtn.addEventListener("click", function () {

        formToDelete = null;

        modal.classList.remove("show");

    });


    /* ================================
       YES
    ================================= */

    yesBtn.addEventListener("click", function () {

        if (!formToDelete) {
            return;
        }

        const form = formToDelete;

        formToDelete = null;

        modal.classList.remove("show");

        HTMLFormElement.prototype.submit.call(form);

    });


    /* ================================
       CLICK OUTSIDE
    ================================= */

    modal.addEventListener("click", function (event) {

        if (event.target === modal) {

            formToDelete = null;

            modal.classList.remove("show");

        }

    });


    /* ================================
       ESCAPE
    ================================= */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            formToDelete = null;

            modal.classList.remove("show");

        }

    });

});

/* =================================
   DELETE TRAINER
================================= */

const trainerModal =
    document.getElementById("deleteTrainerModal");

const trainerNoBtn =
    document.getElementById("deleteTrainerNoBtn");

const trainerYesBtn =
    document.getElementById("deleteTrainerYesBtn");

let trainerFormToDelete = null;


/* ================================
   DELETE TRAINER FORM
================================ */

document.addEventListener("submit", function (event) {

    const form =
        event.target.closest(".delete-trainer-form");

    if (!form) {
        return;
    }

    event.preventDefault();
    event.stopPropagation();

    trainerFormToDelete = form;

    trainerModal.classList.add("show");

});


/* ================================
   NO
================================ */

trainerNoBtn.addEventListener("click", function () {

    trainerFormToDelete = null;

    trainerModal.classList.remove("show");

});


/* ================================
   YES
================================ */

trainerYesBtn.addEventListener("click", function () {

    if (!trainerFormToDelete) {
        return;
    }

    const form =
        trainerFormToDelete;

    trainerFormToDelete = null;

    trainerModal.classList.remove("show");

    HTMLFormElement.prototype.submit.call(form);

});


/* ================================
   CLICK OUTSIDE
================================ */

trainerModal.addEventListener("click", function (event) {

    if (event.target === trainerModal) {

        trainerFormToDelete = null;

        trainerModal.classList.remove("show");

    }

});


/* ================================
   ESCAPE
================================ */

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        trainerFormToDelete = null;

        trainerModal.classList.remove("show");

    }

});