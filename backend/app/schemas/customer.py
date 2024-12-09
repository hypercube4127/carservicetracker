from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
  email = fields.Str(required=True, validate=validate.Length(min=1, max=100), validate=validate.Email())
  phone = fields.Str(required=True, validate=validate.Length(min=1, max=25))
  address = fields.Str(required=True, validate=validate.Length(min=1, max=200))
  comment = fields.Str(validate=validate.Length(max=400))
  
  company_id = fields.Int(required=True)
