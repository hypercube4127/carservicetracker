import logging

from flask import jsonify, g
from werkzeug.exceptions import InternalServerError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from marshmallow import ValidationError

from app.models import InvalidatedToken, User
from app.schemas import BaseResponseSchema, Level

from . import app, jwt, project_config

# Define the logger object
logger = logging.getLogger(__name__)

@app.before_request
def load_user():
  g.app_title = project_config['custom']['app-title']
  try:
    verify_jwt_in_request()
    invalid_token = InvalidatedToken.query.get(get_jwt()['jti'])
    if invalid_token is not None:
      return BaseResponseSchema("Token is invalidated, please log in again.", Level.ERROR).jsonify(), 401
    g.user = User.query.get(get_jwt_identity())
  except Exception as e:
    logger.warning(f"Error loading user: {e}")
    g.user = None

@app.route('/', methods=['GET'])
@app.route('/echo', methods=['GET'])
def echo():
  data = { 
      "version" : project_config['tool']['poetry']['version'],
      "build_number" : project_config['custom']['build-number'],
      "commitid": project_config['custom']['commit-hash']
  } 
  return jsonify(data) 

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
  token_type = jwt_data['type']
  if token_type == 'access':
     return BaseResponseSchema("Token expired, please log in again.", Level.ERROR).jsonify(), 400

@app.errorhandler(Exception)
def handle_exception(e):
  if isinstance(e, ValidationError):
    return BaseResponseSchema(e).jsonify(), 400
  
  if isinstance(e, InternalServerError):
    return BaseResponseSchema(e.description, Level.ERROR).jsonify(), 500
  
  logger.error(f"Error: {e}")
  return BaseResponseSchema(str(e), Level.ERROR).jsonify(), 500
