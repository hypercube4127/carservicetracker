from marshmallow import Schema, fields, validate

class CompanySchema(Schema):
  id = fields.Int(dump_only=True)
  code = fields.Str(dump_only=True)

  name = fields.Str(required=True, validate=validate.Length(min=3))
  email = fields.Email(required=True)
  owner_id = fields.Int(required=True)
  
  address = fields.Str()
  phone_number = fields.Str()
  website = fields.Str()
