from datetime import datetime, timedelta, timezone
from app import db
from enum import Enum

class ConfirmType(Enum):
  CONFIRM_EMAIL = 'user_email'
  MODIFY_EMAIL = 'modify_email'
  REGISTER_COMPANY = 'register_company'
  DELETE_COMPANY = 'delete_company'
  ACCEPT_COMPANY_INVITATION = 'accept_company_invitation'

class Confirm(db.Model):
  __tablename__ = 'confirm'

  code = db.Column(db.String(100), primary_key=True)
  type = db.Column(db.Enum(ConfirmType, native_enum=False), nullable=False)
  name = db.Column(db.String(120), nullable=True)
  email = db.Column(db.String(100), nullable=False)
  expires = db.Column(db.DateTime, nullable=False)
  
  company_name = db.Column(db.String(100), nullable=True)
  user_password = db.Column(db.String(80), nullable=True)
  
  email_sent_at = db.Column(db.DateTime, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
  company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=True)
  
  user = db.relationship('User', backref=db.backref('confirm', lazy=False, cascade='all, delete'))
  company = db.relationship('Company', backref=db.backref('confirm', lazy=False, cascade='all, delete'))
  
  def __init__(self, name, code, type, email, expires=datetime.now(timezone.utc) + timedelta(days=1), company=None, company_name=None, user_password=None, user=None):
      self.user = user
      self.name = name
      self.code = code
      self.type = type
      self.email = email
      self.expires = expires
      self.company = company
      self.company_name = company_name
      self.user_password = user_password

  def __repr__(self):
    return f'<Confirm {self.type} ({self.company_id})>'
  
  def to_dict(self):
    data = {
      'code': self.code,
      'type': self.type,
      'company_id': self.company_id,
      'user_id': self.user_id,
    }
    return data