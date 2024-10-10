from enum import Enum

from flask import jsonify
from marshmallow import ValidationError

from app.schemas.login import LoginSchema
from app.schemas.user import UserSchema
from app.schemas.company import CompanySchema
from app.schemas.site import SiteSchema

class Level(Enum):
  ERROR = "ERROR"
  WARNING = "WARNING"
  INFO = "INFO"
  SUCCESS = "SUCCESS"

class MessageSchema():

  def __init__(self, *args):
    self.message = ""
    self.level = Level.SUCCESS

    for arg in args:
      if type(arg) is str:
        self.message = arg
      elif type(arg) is Level:
        self.level = arg
      else:
        raise TypeError(f"Invalid type: {type(arg)}")

  def set_level(self, level: Level):
    self.level = level

class BaseResponseSchema():

  def __init__(self, *args):
    self.data = {}
    self.messages = []
    self.fielderrors = {}
    self.token = None

    for arg in args:
      if type(arg) is dict:
        self.set_data(arg)
      elif type(arg) is list:
        self.set_data(arg)
      elif type(arg) is str:
        self.add_message(MessageSchema(arg))
      elif type(arg) is list:
        self.add_messages(arg)
      elif type(arg) is MessageSchema:
        self.add_message(arg)
      elif type(arg) is ValidationError:
        self.add_fielderrors(arg)
      elif type(arg) is Level:
        msg = self.messages[len(self.messages) - 1]
        if isinstance(msg, MessageSchema):
          msg.set_level(arg)
      else:
        raise TypeError(f"Invalid type: {type(arg)}")
  
  def add_message(self, message: MessageSchema):
    self.messages.append(message)
  
  def add_messages(self, messages: list):
    self.messages.extend(messages)

  def set_data(self, data: dict):
    self.data = data

  def add_msg(self, message: MessageSchema):
    self.messages.append(message)

  def add_fielderrors(self, error: ValidationError):
    self.fielderrors = error.messages_dict

  def set_token(self, token: str):
    self.token = token

  def to_dict(self):
    return {
      "data": self.data,
      "messages": [ { "message": message.message, "level": message.level.value } for message in self.messages ],
      "fielderrors": self.fielderrors,
      "token": self.token
    }

  def jsonify(self):
    return jsonify(self.to_dict())
