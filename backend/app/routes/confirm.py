from datetime import datetime
from app import app
from app import db
from app.models import Company, User, UserStatus, Confirm, ConfirmType

from app.schemas import BaseResponseSchema, Level

@app.route('/confirm/<string:code>', methods=['GET'])
def confirm(code):
  confirm:Confirm = Confirm.query.get(code)
  if confirm is None:
    return BaseResponseSchema('Invalid confirmation code', Level.ERROR).jsonify(), 400
  
  if confirm.expires < datetime.now():
    db.session.delete(confirm)
    db.session.commit()
    return BaseResponseSchema('Confirmation code expired', Level.ERROR).jsonify(), 400

  type: ConfirmType = confirm.type
  company: Company = confirm.company

  if type == ConfirmType.CONFIRM_EMAIL:
    user: User = confirm.user
    user.status = UserStatus.ACTIVE
    db.session.delete(confirm)
    db.session.add(user)
    db.session.commit()
    return BaseResponseSchema('Email confirmed', Level.SUCCESS).jsonify()
  elif type == ConfirmType.MODIFY_EMAIL:
    user: User = confirm.user
    user.email = confirm.email
    db.session.delete(confirm)
    db.session.add(company)
    db.session.commit()
    return BaseResponseSchema('Email modify successful', Level.SUCCESS).jsonify()
  
  return BaseResponseSchema('Invalid confirmation type', Level.ERROR).jsonify(), 400

def create_confirm(type, user, company=None):
  confirm = Confirm(user=user, type=type, company=company)
  db.session.add(confirm)
  db.session.commit()
  return confirm