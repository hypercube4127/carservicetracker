from .. import db
from enum import Enum

class Company(db.Model):
  __tablename__ = 'company'

  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(5), nullable=False, unique=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 
  address = db.Column(db.String(200), nullable=True)
  email = db.Column(db.String(100), nullable=True, unique=True)
  phone_number = db.Column(db.String(20), nullable=True)
  website = db.Column(db.String(100), nullable=True)
  owner = db.relationship('User', backref=db.backref('company', lazy=True))

  def __repr__(self):
    return f'<Company {self.name} ({self.code})>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'code': self.code,
      'name': self.name,
      'email': self.email,
      'owner_id': self.owner_id,
      'address': self.address,
      'phone_number': self.phone_number,
      'website': self.website,
    }
    return data

class RoleType(Enum):
  ADMIN = "Admin"
  HIGH = "High"
  MEDIUM = "Medium"
  LOW = "Low"
  BASIC = "Basic"

class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Enum(RoleType), nullable=False)
  description = db.Column(db.String(200), nullable=True)

  def __repr__(self):
    return f'<Role {self.name}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'name': self.name,
      'description': self.description,
    }
    return data