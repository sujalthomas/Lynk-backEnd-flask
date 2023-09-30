from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash as encrypt_password
from werkzeug.security import check_password_hash as verify_password
from wtforms import Form, StringField, PasswordField, validators



# MODELS ###############
# Define models #######

#cvs generated
class CoverLetter(db.Model):
    cover_letter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    company_name = db.Column(db.String(100))
    job_listing = db.Column(db.Text)
    recruiter = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=db.func.CURRENT_TIMESTAMP)
    file_path = db.Column(db.String(255))
    user = db.relationship("User", backref="cover_letters")

# resumes uploaded
class Resume(db.Model):
    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="resumes")

# usage statistics
class UsageStatistic(db.Model):
    stat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    action = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=db.func.CURRENT_TIMESTAMP)
    user = db.relationship("User", backref="usage_statistics")

# Define roles
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# user roles
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.user_id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    
    # New columns for reset code and its expiration
    password_reset_code = db.Column(db.String(6))
    password_reset_code_expiration = db.Column(db.DateTime)
    
    # New columns for email verification
    # New columns for authentication and authorization
    is_active = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    verification_code_expiration = db.Column(db.DateTime)

    # New methods and properties for authentication and authorization
    @property
    def active(self):
        return self.is_active

    def get_id(self):
        return self.user_id

    def has_role(self, role):
        return role in [role.name for role in self.roles]




# Define user data store
class UserDatastore:
    def __init__(self, db, user_model, role_model):
        self.db = db
        self.user_model = user_model
        self.role_model = role_model

    def find_user(self, **kwargs):
        return self.user_model.query.filter_by(**kwargs).first()

    def find_role(self, role):
        return self.role_model.query.filter_by(name=role).first()

    def add_role_to_user(self, user, role):
        role = self.find_role(role)
        if role:
            user.roles.append(role)
            self.db.session.commit()

    def remove_role_from_user(self, user, role):
        role = self.find_role(role)
        if role:
            user.roles.remove(role)
            self.db.session.commit()

    def get_user(self, user_id):
        return self.user_model.query.get(user_id)

    def get_role(self, role_id):
        return self.role_model.query.get(role_id)



# Define hashed_password
password = "supersecretpassword"
hashed_password = encrypt_password(password)

# Setup Flask-Security
user_datastore = UserDatastore(db, User, Role)


# Custom registration form
class RegistrationForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    # ...
    # any other fields and validators that you need
    # ...