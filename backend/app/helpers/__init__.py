import random
import string

from app.models import Company, Confirm

def generate_code(code_length=5):
  # FIXME - This is a temporary solution, please use a cache service later
  code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))
  if Company.objects.filter(code=code).exists() or Confirm.objects.filter(code=code).exists():
    return generate_code(code_length)
