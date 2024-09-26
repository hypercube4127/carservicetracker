import bcrypt

from flask import g
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timedelta

from app import app
from app import db
from app import email_service

from app.models import InvalidatedToken, User, UserStatus
from app.schemas import LoginSchema
from app.schemas import BaseResponseSchema, Level

@app.route('/auth/login', methods=['POST'])
def login():
  data = LoginSchema().load(request.json)
  user: User = User.query.filter_by(email=data['email']).first()

  if user.status == UserStatus.INACTIVE:
    return BaseResponseSchema('User is pending, please confirm your email address', Level.ERROR).jsonify(), 400

  if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
    token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
    response = BaseResponseSchema('Successful login', Level.SUCCESS)
    response.set_token(token)
    return response.jsonify()
  
  return BaseResponseSchema('Wrong email or password', Level.ERROR).jsonify(), 400

@app.route('/auth/logout')
@jwt_required()
def logout():
  invalidated = invalitade_token(get_jwt())
  if invalidated is None:
    return BaseResponseSchema('Could not invalidate token', Level.ERROR).jsonify(), 400
  return BaseResponseSchema('Successful logout', Level.SUCCESS).jsonify(), 200

@app.route('/auth/refreshtoken')
@jwt_required()
def refreshtoken():
  jti = get_jwt()['jti']
  new_token = create_access_token(identity=g.user.id, additional_claims={'jti': jti}, expires_delta=timedelta(minutes=30))
  response = BaseResponseSchema()
  response.set_token(new_token)
  return response.jsonify()

def invalitade_token(token: dict):
  if 'jti' not in token or 'exp' not in token:
    app.logger.warning(f"Could not be invalidate token. Wr token or user_id: token={token}")
    return None
  
  InvalidatedToken.query.filter(InvalidatedToken.expiration < datetime.now()).delete()
  expiration = datetime.fromtimestamp(token['exp'])
  invalidate = InvalidatedToken(id=token['jti'], expiration=expiration)
  db.session.add(invalidate)
  db.session.commit()
  return invalidate