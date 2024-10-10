from datetime import datetime
import bcrypt
from flask import request, g
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.helpers import generate_code
from app.schemas import BaseResponseSchema, Level, UserSchema
from app.models import User, Confirm, ConfirmType, UserStatus
from app import app
from app import db
from app.services.email import EmailSenderService
from app.services import user as user_service

@app.route('/user', methods=['GET'])
@jwt_required()
def list_users():
  users = user_service.get_user_relations(g.user.id)
  mapped_users = [user.to_dict() for user in users]
  return BaseResponseSchema(mapped_users).jsonify()

@app.route('/user/<int:id>', methods=['GET', 'PUT'])
@jwt_required()
def get_user(id):
  user: User = User.query.get(id)
  if user is None:
    return BaseResponseSchema("Unauthorized", Level.ERROR).jsonify(), 400
  
  if request.method == 'GET':
    user_service.get_user_relations_ids(g.user.id)
    if g.user.id != id or g.user.id not in user_service.get_user_relations_ids(g.user.id): 
      return BaseResponseSchema("Unauthorized", Level.ERROR).jsonify(), 400
      
    return BaseResponseSchema(user.to_dict()).jsonify()
  elif request.method == 'PUT':
    if g.is_admin is False and g.user.id != user.id:
      return BaseResponseSchema("Unauthorized", Level.ERROR).jsonify(), 400

    data = UserSchema().load(request.json, partial=True, unknown='exclude')
    
    if 'newPassword' in data and data['newPassword'] is not None and len(data['newPassword']) > 8:
      if data['newPassword'] != data['reTypePassword']:
        raise ValidationError('Passwords do not match', 'reTypePassword')
      user.password = bcrypt.hashpw(data['newPassword'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user.fullname = str(data['fullname']).strip()
    
    # TODO Send SMS to user to confirm phone change
    user.phone = data['phone']

    user.country = data['country']
    user.state = data['state']  
    user.city = data['city']
    user.street = data['street']
    user.address = data['address']
    user.zip_code = data['zip_code']

    db.session.add(user)
    response_msg = "Saved succesfully."

    email = str(data['email']).lower().strip()
    if user.email != email:
      if User.query.filter_by(email=email).first():
        db.session.rollback()
        return BaseResponseSchema("User already exists", Level.ERROR).jsonify()
      confirm = Confirm(user=user, name=user.fullname, code=generate_code(), type=ConfirmType.MODIFY_EMAIL, email=email)
      db.session.add(confirm)
      response_msg = "Saved succesfully. Please check your email inbox to finish the email change."
    db.session.commit()
    EmailSenderService.get_instance().send_confirm_emails()
    return BaseResponseSchema(user.to_dict(), response_msg).jsonify()

@app.route('/user', methods=['POST'])
def register():
  if g.user is not None:
    return BaseResponseSchema("You are already logged in, please log out before register a new user.", Level.ERROR).jsonify()
  
  data = UserSchema().load(request.json)
  email = str(data['email']).lower().strip()
  if User.query.filter_by(email=email).first():
    return BaseResponseSchema("User already exists", Level.ERROR).jsonify()
  
  user = User()
  user.email = email
  user.fullname = str(data['fullname']).strip()
  user.status = UserStatus.PENDING
  user.password = bcrypt.hashpw(data['newPassword'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
  
  confirm = Confirm(user=user, name=user.fullname, code=generate_code(), type=ConfirmType.CONFIRM_EMAIL, email=email)
  db.session.add(user)
  db.session.add(confirm)
  db.session.commit()
  EmailSenderService.get_instance().send_confirm_emails()
  return BaseResponseSchema("User registered succesfully").jsonify()