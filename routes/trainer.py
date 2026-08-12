from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from models.user import (
    User,
    TrainerProfile,
    Notice,
    WorkoutRequest,
    MemberWorkout
)

from utils.decorators import (
    login_required,
    role_required
)
from datetime import datetime
from database import db


trainer = Blueprint("trainer", __name__)


# ==========================
# TRAINER PROFILE
# ==========================

@trainer.route("/trainer-profile")
@login_required
@role_required("trainer")
def trainer_profile():
    return render_template("trainer_profile_setup.html")


# ==========================
# TRAINER LANDING
# ==========================

@trainer.route("/trainer")
@login_required
@role_required("trainer")
def trainer_dashboard():

    trainer, profile = (
        db.session.query(User, TrainerProfile)
        .join(
            TrainerProfile,
            TrainerProfile.trainer_id == User.id
        )
        .filter(User.id == session["user_id"])
        .first()
    )

    requests = WorkoutRequest.query.filter_by(
        trainer_id=session["user_id"],
        status="pending"
    ).order_by(
        WorkoutRequest.created_at.desc()
    ).all()

    notices = (
        Notice.query
        .filter(Notice.expires_at > datetime.utcnow())
        .order_by(Notice.created_at.desc())
        .all()
    )

    return render_template(
        "trainer_landing.html",
        trainer=trainer,
        profile=profile,
        notices=notices,
        requests=requests
    )

# ==========================
# TRAINER PROFILE SETUP
# ==========================

@trainer.route("/trainer-profile-setup", methods=["GET", "POST"])
@login_required
@role_required("trainer")
def trainer_profile_setup():

    if request.method == "GET":
        return render_template("trainer_profile_setup.html")

    trainer_id = session["user_id"]

    full_name = request.form["full_name"]
    experience = int(request.form["experience"])

    specializations = request.form.getlist("specialization")
    specialization = ",".join(specializations)

    gender = request.form["gender"]
    bio = request.form["bio"]

    profile = TrainerProfile(
        trainer_id=trainer_id,
        full_name=full_name,
        experience=experience,
        specialization=specialization,
        gender=gender,
        bio=bio
    )

    db.session.add(profile)

    user = User.query.get(trainer_id)
    user.profile_completed = True

    db.session.commit()

    flash("Profile created successfully!", "success")

    return redirect(url_for("trainer.trainer_dashboard"))

@trainer.route("/assign-workout", methods=["POST"])
@login_required
@role_required("trainer")
def assign_workout():

    trainer_id = session["user_id"]

    request_id = request.form.get("request_id")
    workout_day = request.form.get("workout_day")

    exercises = request.form.getlist("exercise[]")
    sets_list = request.form.getlist("sets[]")
    reps_list = request.form.getlist("reps[]")

    if not request_id:
        flash("Invalid workout request.", "error")
        return redirect(url_for("trainer.trainer_dashboard"))

    workout_request = WorkoutRequest.query.filter_by(
        id=request_id,
        trainer_id=trainer_id,
        status="pending"
    ).first()

    if not workout_request:
        flash("Workout request not found or already assigned.", "error")
        return redirect(url_for("trainer.trainer_dashboard"))

    if not workout_day:
        flash("Please enter a workout name.", "error")
        return redirect(url_for("trainer.trainer_dashboard"))

    if not exercises:
        flash("Please add at least one exercise.", "error")
        return redirect(url_for("trainer.trainer_dashboard"))

    if not (
        len(exercises) ==
        len(sets_list) ==
        len(reps_list)
    ):
        flash("Invalid exercise data.", "error")
        return redirect(url_for("trainer.trainer_dashboard"))

    try:

        # Delete old workout
        MemberWorkout.query.filter_by(
            member_id=workout_request.member_id
        ).delete(
            synchronize_session=False
        )

        # Create new workout
        for i in range(len(exercises)):

            exercise_name = exercises[i].strip()
            sets_value = sets_list[i].strip()
            reps_value = reps_list[i].strip()

            if not exercise_name or not sets_value or not reps_value:
                continue

            workout = MemberWorkout(
                request_id=workout_request.id,
                member_id=workout_request.member_id,
                trainer_id=trainer_id,
                exercise=exercise_name,
                exercise_id=None,
                workout_day=workout_day.strip(),
                sets=int(sets_value),
                reps=reps_value
            )

            db.session.add(workout)

        workout_request.status = "assigned"

        db.session.commit()

        flash("Workout assigned successfully!", "success")

    except ValueError:

        db.session.rollback()

        flash("Sets must contain a valid number.", "error")

    except Exception:

        db.session.rollback()

        flash("Something went wrong while assigning the workout.", "error")

    return redirect(url_for("trainer.trainer_dashboard"))