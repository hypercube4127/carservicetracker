import random
import string
from .. import db

from app.models import Company, Confirm

def generate_code(code_length=5):
  # FIXME - This is a temporary solution, please use a cache service later
  code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
  if db.session.query(Company).filter_by(code=code).first() or db.session.query(Confirm).filter_by(code=code).first():
    return generate_code(code_length)
  return code
