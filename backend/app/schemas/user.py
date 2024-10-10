from marshmallow import Schema, fields, validate

class UserSchema(Schema):
  id = fields.Integer(dump_only=True)
  fullname = fields.String(required=True,validate=validate.Length(min=4))
  email = fields.String(required=True,validate=validate.Email())
  phone = fields.String(required=False, allow_none=True)

  newPassword = fields.String(
    required=False, 
    allow_none=True,
    load_only=True, 
    validate=validate.Regexp(
      r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', 
      error="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number."
    )
  )
  reTypePassword = fields.String(required=False, allow_none=True, load_only=True)

  country = fields.String(required=False, allow_none=True)
  state = fields.String(required=False, allow_none=True)
  city = fields.String(required=False, allow_none=True)
  street = fields.String(required=False, allow_none=True)
  address = fields.String(required=False, allow_none=True)
  zip_code = fields.String(required=False, allow_none=True)
