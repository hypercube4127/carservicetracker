from datetime import datetime, timedelta, timezone
from app import db
from enum import Enum

class ConfirmType(Enum):
  CONFIRM_EMAIL = 'user_email'
  MODIFY_EMAIL = 'modify_email'
  DELETE_COMPANY = 'delete_company'
  ACCEPT_COMPANY_INVITATION = 'accept_company_invitation'

class Confirm(db.Model):
  __tablename__ = 'confirm'

  code = db.Column(db.String(5), primary_key=True)
  type = db.Column(db.Enum(ConfirmType), nullable=False)
  name = db.Column(db.String(120), nullable=True)
  email = db.Column(db.String(100), nullable=False)
  expires = db.Column(db.DateTime, nullable=False)
  
  email_sent_at = db.Column(db.DateTime, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
  company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=True)
  
  user = db.relationship('User', backref=db.backref('confirm', lazy=False, cascade='all, delete'))
  company = db.relationship('Company', backref=db.backref('confirm', lazy=False, cascade='all, delete'))
  
  def __init__(self, user, name, code, type, email, expires=datetime.now(timezone.utc) + timedelta(days=1), company=None):
      self.user = user
      self.name = name
      self.code = code
      self.type = type
      self.email = email
      self.expires = expires
      self.company = company

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