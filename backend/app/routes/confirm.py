from datetime import datetime
from flask import request
from app import app
from app import db
from app.helpers import generate_code
from app.models import Company, User, UserStatus, Confirm, ConfirmType, Site, UserSiteUserRole

from app.models.user_site_role import UserRole
from app.routes import CONFIRM_PATH
from app.schemas import BaseResponseSchema, Level

@app.route(f'{CONFIRM_PATH}', methods=['POST'])
def confirm():
  code = request.json.get('code')

  if code is None or code == '':
    return BaseResponseSchema('Confirmation code is required', Level.ERROR).jsonify(), 400
  
  code = code.strip().upper()

  confirm:Confirm = Confirm.query.get(code)
  if confirm is None:
    return BaseResponseSchema('Invalid confirmation code', Level.ERROR).jsonify(), 400
  
  if confirm.expires < datetime.now():
    db.session.delete(confirm)
    db.session.commit()
    return BaseResponseSchema('Confirmation code expired', Level.ERROR).jsonify(), 400

  type: ConfirmType = confirm.type
  if type == ConfirmType.CONFIRM_EMAIL:
    user: User = confirm.user
    user.status = UserStatus.ACTIVE
    db.session.delete(confirm)
    db.session.add(user)
    db.session.commit()
    db.session.delete(confirm)
    return BaseResponseSchema('Email confirmed', Level.SUCCESS).jsonify()
  if type == ConfirmType.REGISTER_COMPANY:
    user: User = User(fullname=confirm.name, email=confirm.email, status=UserStatus.ACTIVE, password=confirm.user_password)
    company = Company(name=confirm.company_name, code=generate_code(), owner=user)
    default_site: Site = Site(name=f"{company.name} first site", company=company)
    site_role = UserSiteUserRole(user=user, site=default_site, role=UserRole.ADMIN)

    db.session.add(user)
    db.session.add(company)
    db.session.add(default_site)
    db.session.add(site_role)
    db.session.commit()
    db.session.delete(confirm)
    return BaseResponseSchema('Your company created', Level.SUCCESS).jsonify()
  elif type == ConfirmType.MODIFY_EMAIL:
    user: User = confirm.user
    user.email = confirm.email
    db.session.delete(confirm)
    db.session.commit()
    db.session.delete(confirm)
    return BaseResponseSchema('Email modify successful', Level.SUCCESS).jsonify()
  
  return BaseResponseSchema('Invalid confirmation type', Level.ERROR).jsonify(), 400

def create_confirm(type, user, company=None):
  confirm = Confirm(user=user, type=type, company=company)
  db.session.add(confirm)
  db.session.commit()
  return confirm