from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=4),load_only=True)