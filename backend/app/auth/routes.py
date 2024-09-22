import bcrypt

from flask import g
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timedelta

from app import app

from app.auth.schemas import LoginSchema
from app.schemas import BaseResponseSchema, Level
from app.users.models import User

@app.route('/auth/login', methods=['POST'])
def login():
  data = LoginSchema().load(request.json)
  user = User.query.filter_by(email=data['email']).first()

  if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
    token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
    response = BaseResponseSchema('Successful login', Level.SUCCESS)
    response.set_token(token)
    return response.jsonify()
  
  return BaseResponseSchema('Wrong email or password', Level.ERROR).jsonify(), 400

@app.route('/auth/logout')
@jwt_required()
def logout():
  return BaseResponseSchema('Successful logout', Level.SUCCESS).jsonify(), 400

@app.route('/auth/refreshtoken')
@jwt_required()
def refreshtoken():
  jti = get_jwt()['jti']
  new_token = create_access_token(identity=g.user.id, additional_claims={'jti': jti}, expires_delta=timedelta(minutes=30))
  response = BaseResponseSchema()
  response.set_token(new_token)
  return response.jsonify()
