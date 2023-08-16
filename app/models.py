from . import db
from flask_security import UserMixin, RoleMixin

class CoverLetter(db.Model):
    cover_letter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    company_name = db.Column(db.String(100))
    job_listing = db.Column(db.Text)
    recruiter = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=db.func.current())
    file_path = db.Column(db.String(255))
    user = db.relationship("User", backref="cover_letters")

class Resume(db.Model):
    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=db.func.current())
    user = db.relationship("User", backref="resumes")

class UsageStatistic(db.Model):
    stat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    action = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=db.func.current())
    user = db.relationship("User", backref="usage_statistics")

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.user_id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
