from marshmallow import Schema, fields, validate

class CarSchema(Schema):
  id = fields.Int(dump_only=True)
  vin = fields.Str(required=True, validate=validate.Length(min=17, max=17))
  model = fields.Str(required=True, validate=validate.Length(min=1, max=100))
  make = fields.Str(required=True, validate=validate.Length(min=1, max=100))
  year = fields.Int(required=False, allow_none=True)

  plate = fields.Str(required=False, allow_none=True)
  engine_number = fields.Str(required=False, allow_none=True)
  engine_code = fields.Str(required=False, allow_none=True)
  power = fields.Int(required=False, allow_none=True)

  company_id = fields.Int(required=True)

class VmiDecodeResult():
  manufacturer: str
  model: str
  year: int

  def __init__(self, manufacturer: str, model: str, year: int):
    self.manufacturer = manufacturer
    self.model = model
    self.year = year
  
  def to_dict(self):
    return {
      'manufacturer': self.manufacturer,
      'model': self.model,
      'year': self.year
    }