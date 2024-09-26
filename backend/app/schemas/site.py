from marshmallow import Schema, fields, validate

class SiteSchema(Schema):
  id = fields.Int(required=True)
  name = fields.Str(required=True, validate=validate.Length(min=1))
  address = fields.Str()
  email = fields.Email()
  company_id = fields.Int(required=True)
  