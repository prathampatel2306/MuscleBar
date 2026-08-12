from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # Onboarding
    profile_completed = db.Column(db.Boolean, default=False)
    membership_plan = db.Column(db.String(30), nullable=True)

    # Member Profile
    full_name = db.Column(db.String(100), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    height = db.Column(db.Float, nullable=True)  # cm
    weight = db.Column(db.Float, nullable=True)  # kg
    experience_level = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    membership_start_date = db.Column(db.Date)
    membership_end_date = db.Column(db.Date)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class TrainerAssignment(db.Model):
    __tablename__ = "trainer_assignments"

    id = db.Column(db.Integer, primary_key=True)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    trainer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    assigned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class TrainerProfile(db.Model):
    __tablename__ = "trainer_profiles"

    id = db.Column(db.Integer, primary_key=True)

    trainer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(db.String(100), nullable=False)

    experience = db.Column(db.Integer, nullable=False)

    specialization = db.Column(db.String(255), nullable=False)

    gender = db.Column(db.String(20), nullable=False)

    bio = db.Column(db.Text, nullable=False)

from datetime import datetime, timedelta
from database import db


class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=7)
    )

class WorkoutRequest(db.Model):
    __tablename__ = "workout_requests"

    id = db.Column(db.Integer, primary_key=True)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trainer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        "requested_at",
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    member = db.relationship(
        "User",
        foreign_keys=[member_id]
    )

    trainer = db.relationship(
        "User",
        foreign_keys=[trainer_id]
    )

class MemberWorkout(db.Model):
    __tablename__ = "member_workouts"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_requests.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trainer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    exercise = db.Column(
        db.String(100),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        nullable=True
    )

    workout_day = db.Column(
        db.String(100),
        nullable=False
    )

    sets = db.Column(
        db.Integer,
        nullable=False
    )

    reps = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )