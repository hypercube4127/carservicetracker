from .. import db

class Car(db.Model):
  __tablename__ = 'car'

  id = db.Column(db.Integer, primary_key=True)
  vin = db.Column(db.String(100), nullable=False)
  model = db.Column(db.String(100), nullable=False)
  make = db.Column(db.String(100), nullable=False)
  year = db.Column(db.Integer, nullable=False)

  plate = db.Column(db.String(100), nullable=False)
  plate_normalized = db.Column(db.String(100), nullable=False)
  engine_number = db.Column(db.String(100), nullable=False)
  engine_code = db.Column(db.String(100), nullable=False)
  power = db.Column(db.Integer, nullable=False)
  technical_exam_expiration = db.Column(db.DateTime, nullable=True)

  company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
  company = db.relationship('Company', backref=db.backref('car', lazy=True))

  def __repr__(self):
    return f'<Car {self.name}>'

  def to_dict(self):
    data = {
      'id': self.id,
      'vin': self.vin,
      'model': self.model,
      'make': self.make,
      'year': self.year,
      'plate': self.plate,
      'plate_normalized': self.plate_normalized,
      'engine_number': self.engine_number,
      'engine_code': self.engine_code,
      'power': self.power,
      'technical_exam_expiration': self.technical_exam_expiration,
      'company_id': self.company_id
    }
    return data

class Wmi(db.Model):
  __tablename__ = 'wmi'

  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(3), nullable=False, unique=True)
  manufacturer = db.Column(db.String(100), nullable=False)

  def __init__(self, code, manufacturer):
    self.code = code
    self.manufacturer = manufacturer

  def __repr__(self):
    return f'<Wmi {self.code} {self.manufacturer}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'code': self.code,
      'manufacturer': self.manufacturer
    }
    return data

class Vds(db.Model):
  __tablename__ = 'vds'

  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(6), nullable=False, unique=True)
  model = db.Column(db.String(100), nullable=False)

  def __init__(self, code, model):
    self.code = code
    self.model = model

  def __repr__(self):
    return f'<Vds {self.code} {self.model}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'code': self.code,
      'model': self.model
    }
    return data

class Year(db.Model):
  __tablename__ = 'year'

  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(1), nullable=False, unique=True)
  year = db.Column(db.Integer, nullable=False)

  def __init__(self, code, year):
    self.code = code
    self.year = year

  def __repr__(self):
    return f'<Year {self.code} {self.year}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'code': self.code,
      'year': self.year
    }
    return data