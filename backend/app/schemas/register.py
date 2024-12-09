from marshmallow import Schema, fields, validate

class RegisterCompanySchema(Schema):
  id = fields.Integer(dump_only=True)

  name = fields.String(required=True,validate=validate.Length(min=4))
  email = fields.String(required=True,validate=validate.Email())
  password = fields.String(
    required=False, 
    allow_none=True,
    load_only=True, 
    validate=validate.Regexp(
      r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', 
      error="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number."
    )
  )
  reTypePassword = fields.String(required=False, allow_none=True, load_only=True)

  companyName = fields.String(required=True,validate=validate.Length(min=4,max=100))
