from marshmallow import Schema, fields, validate

class ServiceSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
  price_netto = fields.Float(required=True)
  tax = fields.Float(required=True)
  price_brutto = fields.Float(required=True)
  duty = fields.Float(required=False, allow_none=True)
  description = fields.Str(required=False, allow_none=True)

  company_id = fields.Int(required=True)
