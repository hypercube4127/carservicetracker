from .. import db
from enum import Enum

class UserStatus(Enum):
  PENDING = "pending"
  ACTIVE = "active"
  INACTIVE = "inactive"
  BANNED = "banned"

class User(db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  
  fullname = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  status = db.Column(db.Enum(UserStatus), default=UserStatus.INACTIVE, nullable=False)
  password = db.Column(db.String(80), nullable=False)

  phone = db.Column(db.String(20), nullable=True)
  country = db.Column(db.String(120), nullable=True)
  state = db.Column(db.String(120), nullable=True)
  city = db.Column(db.String(120), nullable=True)
  street = db.Column(db.String(120), nullable=True)
  address = db.Column(db.String(120), nullable=True)
  zip_code = db.Column(db.String(10), nullable=True)

  is_active = db.Column(db.Boolean(), default=True)

  sites = db.relationship('Site', secondary='user_site', back_populates='users')


  def __repr__(self):
    return f'<User {self.email}>'

  def to_dict(self):
    data = {
      'id': self.id,
      
      'fullname': self.fullname,
      'email': self.email,
      'phone': self.phone,

      'country': self.country,
      'state': self.state,
      'city': self.city,
      'street': self.street,
      'address': self.address,
      'zip_code': self.zip_code,
    }
    return data