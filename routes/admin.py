from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta,date

from database import db
from models.user import  User,Notice,TrainerProfile,TrainerAssignment
from utils.decorators import login_required, role_required

admin = Blueprint("admin", __name__)



# ==========================
# ADMIN LANDING
# ==========================
@admin.route("/admin")
@login_required
@role_required("admin")
def admin_landing():

    member_count = User.query.filter_by(role="member").count()
    trainer_count = User.query.filter_by(role="trainer").count()
    members = User.query.filter_by(role="member").all()
    trainer_profiles = TrainerProfile.query.all()

    return render_template(
        "admin_landing.html",
        member_count=member_count,
        trainer_count=trainer_count,
        members=members,
        trainer_profiles=trainer_profiles
    )


# ==========================
# ADMIN DASHBOARD
# ==========================
@admin.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():


    today = date.today()

    # -------------------------
    # ACTIVE MEMBERS
    # -------------------------

    active_member_count = User.query.filter(
        User.role == "member",
        User.membership_end_date >= today
    ).count()

    # -------------------------
    # TOTAL REVENUE YTD
    # -------------------------

    plan_prices = {
        "3 Months": 5000,
        "6 Months": 7000,
        "12 Months": 10000
    }

    ytd_members = User.query.filter(
        User.role == "member",
        User.membership_start_date >= date(today.year, 1, 1),
        User.membership_start_date <= today
    ).all()

    total_revenue = sum(
        plan_prices.get(member.membership_plan, 0)
        for member in ytd_members
    )

    # -------------------------
    # TRAINER UTILIZATION
    # -------------------------

    total_trainer_count = User.query.filter_by(
        role="trainer"
    ).count()

    assigned_trainer_ids = {
        assignment.trainer_id
        for assignment in TrainerAssignment.query.all()
    }

    assigned_trainer_count = len(assigned_trainer_ids)

    trainer_utilization = (
        round(
            (assigned_trainer_count / total_trainer_count) * 100,
            1
        )
        if total_trainer_count > 0
        else 0
    )

    # =========================
    # TRAINER PERFORMANCE
    # =========================

    trainer_performance = []

    trainer_profiles = TrainerProfile.query.all()

    for trainer in trainer_profiles:

        member_count = TrainerAssignment.query.filter_by(
            trainer_id=trainer.trainer_id
        ).count()

        trainer_performance.append({
            "name": trainer.full_name or "Trainer",
            "specialization": trainer.specialization or "Fitness",
            "member_count": member_count
        })

    # Show trainers with the highest number of assigned members first
    trainer_performance.sort(
        key=lambda x: x["member_count"],
        reverse=True
    )

    # Keep the dashboard card compact
    trainer_performance = trainer_performance[:4]

    max_trainer_members = max(
        [trainer["member_count"] for trainer in trainer_performance],
        default=0
    )

    # =========================
    # MEMBERSHIP DISTRIBUTION
    # =========================

    membership_plans = [
        "12 Months",
        "6 Months",
        "3 Months"
    ]

    membership_distribution = []

    total_members = User.query.filter_by(
        role="member"
    ).count()

    for plan in membership_plans:

        count = User.query.filter(
            User.role == "member",
            User.membership_plan == plan
        ).count()

        percentage = (
            round((count / total_members) * 100, 1)
            if total_members > 0
            else 0
        )

        membership_distribution.append({
            "plan": plan,
            "count": count,
            "percentage": percentage
        })

    # =========================
    # REVENUE TREND
    # =========================

    current_year = date.today().year
    current_month = date.today().month

    plan_prices = {
        "3 Months": 5000,
        "6 Months": 7000,
        "12 Months": 10000
    }

    monthly_revenue = []

    members = User.query.filter(
        User.role == "member",
        User.membership_plan.isnot(None),
        User.membership_start_date.isnot(None)
    ).all()

    for month in range(1, 13):

        if month > current_month:
            monthly_revenue.append(None)
            continue

        revenue = 0

        for member in members:

            start_date = member.membership_start_date

            if (
                    start_date.year == current_year
                    and start_date.month == month
            ):
                revenue += plan_prices.get(
                    member.membership_plan,
                    0
                )
        monthly_revenue.append(revenue)

    # =========================
    # MEMBERSHIP GROWTH
    # =========================

    current_year = date.today().year

    membership_growth = []

    for year in range(current_year - 2, current_year + 1):

        count = User.query.filter(
            User.role == "member",
            User.membership_start_date.isnot(None),
            db.extract("year", User.membership_start_date) == year
        ).count()

        membership_growth.append({
            "year": year,
            "count": count
        })

    # Growth compared with previous year
    previous_year_count = membership_growth[-2]["count"]
    current_year_count = membership_growth[-1]["count"]

    if previous_year_count > 0:
        growth_percentage = round(
            ((current_year_count - previous_year_count)
             / previous_year_count) * 100,
            1
        )
    else:
        growth_percentage = None

    return render_template(
        "admin_dashboard.html",
        total_revenue=total_revenue,
        active_member_count=active_member_count,
        trainer_utilization=trainer_utilization,
        assigned_trainer_count=assigned_trainer_count,
        total_trainer_count=total_trainer_count,
        monthly_revenue=monthly_revenue,
        dashboard_year=current_year,
        membership_distribution=membership_distribution,
        membership_growth=membership_growth,
        growth_percentage=growth_percentage,
        trainer_performance=trainer_performance,
        max_trainer_members=max_trainer_members
    )

# ==========================
# PUBLISH NOTICE
# ==========================
@admin.route("/admin/publish_notice", methods=["POST"])
@login_required
@role_required("admin")
def publish_notice():

    message = request.form.get("message", "").strip()

    if not message:
        flash("Notice cannot be empty.", "error")
        return redirect(url_for("admin.admin_landing"))

    notice = Notice(
        message=message,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.session.add(notice)
    db.session.commit()

    flash("Notice published successfully!", "success")
    return redirect(url_for("admin.admin_landing"))

@admin.route("/admin/delete-member/<int:member_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_member(member_id):
    member = User.query.get_or_404(member_id)

    db.session.delete(member)
    db.session.commit()

    return redirect(url_for("admin.admin_landing"))

@admin.route("/admin/delete-trainer/<int:trainer_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_trainer(trainer_id):
    trainer = TrainerProfile.query.filter_by(trainer_id=trainer_id).first_or_404()
    user = User.query.get_or_404(trainer.trainer_id)

    db.session.delete(trainer)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("admin.admin_landing"))