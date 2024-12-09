from marshmallow import Schema, fields, validate

class CompanySchema(Schema):
  id = fields.Int(dump_only=True)
  code = fields.Str(dump_only=True)

  name = fields.Str(required=True, validate=validate.Length(min=3))
  email = fields.Email(required=False, allow_none=True, validate=validate.Email())
  
  address = fields.Str(required=False, allow_none=True)
  phone_number = fields.Str(required=False, allow_none=True, validate=validate.Regexp(r'^\+?1?\d{9,15}$'))
  website = fields.Str(required=False, allow_none=True, validate=validate.URL())
