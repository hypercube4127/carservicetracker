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
  invited_email = db.Column(db.String(100), nullable=True)
  expires = db.Column(db.DateTime, nullable=False, default=db.func.now())
  
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
  company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
  

  user = db.relationship('User', backref=db.backref('confirm', lazy=False))
  company = db.relationship('Company', backref=db.backref('confirm', lazy=False))
  
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