from .. import db

class Site(db.Model):
  __tablename__ = 'site'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  url = db.Column(db.String(200), nullable=False)
  company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
  company = db.relationship('Company', backref=db.backref('site', lazy=True))
  users = db.relationship('User', secondary='user_site', back_populates='sites') 

  def __repr__(self):
    return f'<Site {self.name}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'name': self.name,
      'url': self.url,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }
    return data

  

