from app import db

class Customer(db.Model):
  __tablename__ = 'customer'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), primary_key=True)
  email = db.Column(db.String(100), nullable=False)
  phone = db.Column(db.String(25), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  comment = db.Column(db.String(400), nullable=True)

  company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
  company = db.relationship('Company', backref=db.backref('customer', lazy=False, cascade='all, delete'))

  def __repr__(self):
    return f'<Cusomer {self.name} ({self.company_id})>'
  
  def to_dict(self):
    data = {
      'name': self.name,
      'email': self.email,
      'phone': self.phone,
      'address': self.address,
      'comment': self.comment,
      'company_id': self.company_id
    }
    return data