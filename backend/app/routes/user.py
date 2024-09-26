import bcrypt
from flask import jsonify, request, g
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.helpers import generate_code
from app.schemas import BaseResponseSchema, Level, UserSchema
from app.models import User, Confirm, ConfirmType
from app import app
from app import db
from app import email_service

@app.route('/user', methods=['GET'])
@jwt_required()
def list_users():
  users = User.query.all()
  mapped_users = [user.to_dict() for user in users]
  return BaseResponseSchema(mapped_users).jsonify()

@app.route('/user/<int:id>', methods=['GET', 'PUT'])
@jwt_required()
def get_user(id):
  user: User = User.query.get(id)
  if request.method == 'GET':
    return BaseResponseSchema(user.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = UserSchema().load(request.json, partial=True, unknown='exclude')
    
    if 'newPassword' in data and data['newPassword'] is not None and len(data['newPassword']) > 8:
      if data['newPassword'] != data['reTypePassword']:
        raise ValidationError('Passwords do not match', 'reTypePassword')
      user.password = bcrypt.hashpw(data['newPassword'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user.email = data['email']
    user.fullname = data['fullname']
    
    # TODO Send email to user to confirm email change
    user.email = data['email']
    # TODO Send SMS to user to confirm phone change
    user.phone = data['phone']

    user.country = data['country']
    user.state = data['state']  
    user.city = data['city']
    user.street = data['street']
    user.address = data['address']
    user.zip_code = data['zip_code']

    db.session.commit()
    return BaseResponseSchema(user.to_dict(), "Saved succesfully").jsonify()

@app.route('/user', methods=['POST'])
def register():
  data = UserSchema().load(request.json)
  
  if User.query.filter_by(email=data['email']).first():
    return BaseResponseSchema(None, "User already exists", level=Level.ERROR).jsonify()
  
  user = User(**data)
  user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
  
  confirm = Confirm(user=user, code=generate_code(), type=ConfirmType.CONFIRM_EMAIL).save()

  email_service.send_confirm_email(confirm)

  db.session.add(user)
  db.session.commit()
  return BaseResponseSchema(user.to_dict(), "Created succesfully").jsonify()