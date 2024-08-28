from flask_login import UserMixin
from core import db
from sqlalchemy.sql import func
import datetime
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), nullable = True)
    email = db.Column(db.String(50), unique = True )
    password = db.Column(db.String(50), nullable = True)
    # created_on = db.Column(db.DateTime, nullable=False)
    # is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    # confirmed_on = db.Column(db.DateTime, nullable=True)

    
  
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return f' username: {self.user_name}'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable = True)
    email = db.Column(db.String(50), unique = True )
    amount = db.Column(db.String(50), nullable = True)
   