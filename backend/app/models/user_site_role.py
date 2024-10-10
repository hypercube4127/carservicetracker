from .. import db
from enum import Enum

class UserRole(Enum):
  ADMIN = "Admin"
  HIGH = "High"
  MEDIUM = "Medium"
  LOW = "Low"
  BASIC = "Basic"

class UserSiteUserRole(db.Model):
  __tablename__ = 'user_site_role'

  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
  site_id = db.Column(db.Integer, db.ForeignKey('site.id', ondelete='CASCADE'), primary_key=True)
  role = db.Column(db.Enum(UserRole), nullable=False)
  
  user = db.relationship('User', backref=db.backref('user_site_role', lazy=True))
  site = db.relationship('Site', backref=db.backref('user_site_role', lazy=True))
  
  def __repr__(self):
    return f'<UserSiteUserRole {self.user_id} - {self.site_id} - {self.role}>'
  
  def to_dict(self):
    data = {
      'user_id': self.user_id,
      'site_id': self.site_id,
      'role': self.role,
    }
    return data