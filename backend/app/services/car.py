import re

import requests

from app.models.car import Vds, Wmi, Year

def normalize_plate(plate):
    return re.sub(r'[^A-Z0-9]', '', plate.upper())

def vin_decode(vin):
  wmi = vin[:3]
  vds = vin[3:9]
  year_code = vin[9]
  wmi_cache: Wmi = Wmi.query.filter_by(code=wmi).first()
  if wmi_cache is not None:
    vds_cache: Vds = Vds.query.filter_by(code=vds).first()
    if vds_cache is not None:
      year_cache: Year = Year.query.filter_by(code=year_code).first()
      if year_cache is not None:
          return {
            'manufacturer': wmi_cache.manufacturer,
            'model': vds_cache.model,
            'year': year_cache.year
          }

  url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json'
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    
    manufacturer = None
    model = None
    year = None

    for item in data['Results']:
      if item['Variable'] == 'Make':
        manufacturer = item['Value']
      elif item['Variable'] == 'Model':
        model = item['Value']
      elif item['Variable'] == 'Model Year':
        year = item['Value']
    
    return {
            'manufacturer': manufacturer,
            'model': model,
            'year': year
    }
  else:
    return None