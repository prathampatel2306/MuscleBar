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
    TrainerAssignment,
    TrainerProfile,
    Notice,
    WorkoutRequest,
    MemberWorkout
)

from datetime import datetime, timedelta,date
from database import db
from utils.decorators import login_required, role_required

# Create Member Blueprint
member = Blueprint("member", __name__)


# =====================================================
# MEMBERSHIP PLAN
# =====================================================

@member.route("/plan", methods=["GET", "POST"])
@login_required
@role_required("member")
def plan():

    from datetime import datetime, timedelta

    # Get the logged-in user
    user = User.query.get(session["user_id"])

    # ==========================
    # Handle Plan Selection
    # ==========================
    if request.method == "POST":

        selected_plan = request.form.get("plan")

        valid_plans = [
            "3 Months",
            "6 Months",
            "12 Months"
        ]

        if selected_plan not in valid_plans:
            flash("Invalid membership plan selected.", "error")
            return redirect(url_for("member.plan"))

        # Save selected plan
        user.membership_plan = selected_plan

        # --------------------------
        # Existing Member (Renewal)
        # --------------------------
        if user.profile_completed:

            today = datetime.today().date()

            user.membership_start_date = today

            if selected_plan == "3 Months":
                user.membership_end_date = today + timedelta(days=90)

            elif selected_plan == "6 Months":
                user.membership_end_date = today + timedelta(days=180)

            elif selected_plan == "12 Months":
                user.membership_end_date = today + timedelta(days=365)

            db.session.commit()

            flash("Membership renewed successfully!", "success")

            return redirect(url_for("member.member_dashboard"))

        # --------------------------
        # New Member
        # --------------------------
        db.session.commit()

        flash("Membership Plan Selected Successfully!", "success")

        return redirect(url_for("member.profile_setup"))

    # GET Request
    return render_template("plan.html")

# =====================================================
# PROFILE SETUP
# =====================================================

@member.route("/profile-setup", methods=["GET", "POST"])
@login_required
@role_required("member")
def profile_setup():

    # Get logged-in user
    user = User.query.get(session["user_id"])

    # If profile already completed, go to dashboard
    if user.profile_completed:
        return redirect(url_for("member.member_dashboard"))

    if request.method == "POST":

        # Read form data
        user.full_name = request.form.get("full_name")
        user.date_of_birth = request.form.get("date_of_birth")
        user.gender = request.form.get("gender")

        # Convert numeric values
        height = request.form.get("height")
        weight = request.form.get("weight")

        user.height = float(height) if height else None
        user.weight = float(weight) if weight else None

        user.experience_level = request.form.get("experience_level")

        today = datetime.today().date()

        user.membership_start_date = today

        if user.membership_plan == "3 Months":
            user.membership_end_date = today + timedelta(days=90)

        elif user.membership_plan == "6 Months":
            user.membership_end_date = today + timedelta(days=180)

        elif user.membership_plan == "12 Months":
            user.membership_end_date = today + timedelta(days=365)

        # Mark onboarding complete
        user.profile_completed = True

        # Save changes
        db.session.commit()

        flash("Profile setup completed successfully!", "success")

        return redirect(url_for("member.member_dashboard"))

    return render_template("profile_setup.html")


# =====================================================
# MEMBER DASHBOARD
# =====================================================

@member.route("/member")
@login_required
@role_required("member")
def member_dashboard():

    # Logged-in member
    user = User.query.get(session["user_id"])
    workouts = MemberWorkout.query.filter_by(
        member_id=user.id
    ).order_by(
        MemberWorkout.created_at.desc()
    ).all()

    # Greeting
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # BMI
    bmi = None
    if user.height and user.weight:
        bmi = round(user.weight / ((user.height / 100) ** 2), 1)

    today = date.today()

    status = "No Membership"
    remaining_days = 0
    progress_percentage = 0
    expiry_date = None

    if user.membership_start_date and user.membership_end_date:

        expiry_date = user.membership_end_date.strftime("%d %b %Y")

        total_days = (
                user.membership_end_date - user.membership_start_date
        ).days

        remaining_days = (
                user.membership_end_date - today
        ).days

        if remaining_days < 0:
            remaining_days = 0

        if today > user.membership_end_date:
            status = "Expired"

        elif today == user.membership_end_date:
            status = "Expires Today"

        else:
            status = "Active"

        elapsed_days = total_days - remaining_days

        progress_percentage = (
                                      elapsed_days / total_days
                              ) * 100 if total_days > 0 else 0

        progress_percentage = min(progress_percentage, 100)

    # Fetch all registered trainers
    trainers = User.query.filter_by(role="trainer").all()

    notices = (
        Notice.query
        .filter(Notice.expires_at > datetime.utcnow())
        .order_by(Notice.created_at.desc())
        .all()
    )

    

    return render_template(
        "member_landing.html",
        user=user,
        greeting=greeting,
        bmi=bmi,
        trainers=trainers,
        status=status,
        expiry_date=expiry_date,
        remaining_days=remaining_days,
        progress_percentage=progress_percentage,
        notices=notices,
        workouts=workouts,
    )

@member.route("/select-trainer")
@login_required
@role_required("member")
def select_trainer():

    member_id = session["user_id"]

    # Check if member already has a trainer
    assignment = TrainerAssignment.query.filter_by(
        member_id=member_id
    ).first()

    # If trainer is already assigned, don't ask again
    if assignment:
        return redirect(url_for("member.view_trainer"))

    trainers = (
        db.session.query(User, TrainerProfile)
        .join(
            TrainerProfile,
            TrainerProfile.trainer_id == User.id
        )
        .filter(User.role == "trainer")
        .all()
    )

    return render_template(
        "select_trainer.html",
        trainers=trainers
    )

@member.route("/assign-trainer/<int:trainer_id>")
@login_required
@role_required("member")
def assign_trainer(trainer_id):

    member_id = session["user_id"]

    # Check if the member already has a trainer
    assignment = TrainerAssignment.query.filter_by(member_id=member_id).first()

    if assignment:
        # Update existing trainer
        assignment.trainer_id = trainer_id

    else:
        # First-time assignment
        assignment = TrainerAssignment(
            member_id=member_id,
            trainer_id=trainer_id
        )
        db.session.add(assignment)

    db.session.commit()

    flash("Trainer updated successfully!", "success")

    return redirect(url_for("member.view_trainer"))


@member.route("/view-trainer")
@login_required
@role_required("member")
def view_trainer():

    member_id = session["user_id"]

    # Get assigned trainer
    assignment = TrainerAssignment.query.filter_by(
        member_id=member_id
    ).first()

    if not assignment:
        flash("Please select a trainer first.", "info")
        return redirect(url_for("member.select_trainer"))

    # Fetch trainer and profile
    trainer, profile = (
        db.session.query(User, TrainerProfile)
        .join(
            TrainerProfile,
            TrainerProfile.trainer_id == User.id
        )
        .filter(User.id == assignment.trainer_id)
        .first()
    )

    return render_template(
        "view_trainer.html",
        trainer=trainer,
        profile=profile
    )

@member.route("/change-trainer")
@login_required
@role_required("member")
def change_trainer():

    trainers = (
        db.session.query(User, TrainerProfile)
        .join(
            TrainerProfile,
            TrainerProfile.trainer_id == User.id
        )
        .filter(User.role == "trainer")
        .all()
    )

    return render_template(
        "select_trainer.html",
        trainers=trainers
    )

@member.route("/request-workout", methods=["POST"])
@login_required
@role_required("member")
def request_workout():

    member_id = session["user_id"]

    assignment = TrainerAssignment.query.filter_by(
        member_id=member_id
    ).first()

    if not assignment:
        flash("Please select a trainer first.", "error")
        return redirect(url_for("member.member_dashboard"))

    existing_request = WorkoutRequest.query.filter_by(
        member_id=member_id,
        trainer_id=assignment.trainer_id,
        status="pending"
    ).first()

    if existing_request:
        flash("You already have a pending workout request.", "info")
        return redirect(url_for("member.member_dashboard"))

    workout_request = WorkoutRequest(
        member_id=member_id,
        trainer_id=assignment.trainer_id,
        status="pending"
    )

    db.session.add(workout_request)
    db.session.commit()

    flash("Workout request sent to your trainer!", "success")

    return redirect(url_for("member.member_dashboard"))