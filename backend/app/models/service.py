from app import db

class Service(db.Model):
  __tablename__ = 'service'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), primary_key=True)
  price_netto = db.Column(db.Float, nullable=False)
  tax = db.Column(db.Float, nullable=False)
  price_brutto = db.Column(db.Float, nullable=False)
  duty = db.Column(db.Float, nullable=False, default=0)
  description = db.Column(db.String(400), nullable=True)

  site_id = db.Column(db.Integer, db.ForeignKey('site.id', ondelete='CASCADE'), nullable=True)
  site = db.relationship('Site', backref=db.backref('service', lazy=False, cascade='all, delete'))
  
  company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
  company = db.relationship('Company', backref=db.backref('service', lazy=False, cascade='all, delete'))

  def __repr__(self):
    return f'<Service {self.name} ({self.company_id})>'
  
  def to_dict(self):
    data = {
      'name': self.name,
      'price_netto': self.price_netto,
      'tax': self.tax,
      'price_brutto': self.price_brutto,
      'duty': self.duty,
      'description': self.description,
      'company_id': self.company_id
    }
    return data