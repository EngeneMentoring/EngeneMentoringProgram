from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    private = db.Column(db.Boolean, default=False)
    adminStatus = db.Column(db.Integer, default=0)
    """
    0 - Pending Approval from Admin
    1 - Accepted by Admin
    2 - Rejected by Admin
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    capsuleId = db.Column(db.String(150))
    # status=db.Column(db.String(150))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    school_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    admin = db.Column(db.Boolean,default=False)