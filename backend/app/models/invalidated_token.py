from .. import db

class InvalidatedToken(db.Model):
  __tablename__ = 'invalidated_token'

  id = db.Column(db.String(200), primary_key=True)
  expiration = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<InvalidatedToken {self.token_id}>'
  
  def to_dict(self):
    data = {
      'id': self.id,
      'expiration': self.expiration,
    }
    return data