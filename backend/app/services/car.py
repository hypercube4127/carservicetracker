import re

import requests

from app.models.car import Vds, Wmi, Year
from app.schemas.car import VmiDecodeResult
from app import db

def normalize_plate(plate):
    return re.sub(r'[^A-Z0-9]', '', plate.upper())

def vin_decode(vin):
  
  result = VmiDecodeResult(None, None, None)
  wmi = None
  vds = None
  year_code = None

  if len(vin) >= 3:
    wmi = vin[:3]
    wmi_cache: Wmi = Wmi.query.filter_by(code=wmi).first()
    if wmi_cache:
      result.manufacturer = wmi_cache.manufacturer
  
  if len(vin) >= 9:
    vds = vin[3:9]
    vds_cache: Vds = Vds.query.filter_by(code=vds).first()
    if vds_cache:
      result.model = vds_cache.model

    year_code = vin[9]
    year_cache: Year = Year.query.filter_by(code=year_code).first()
    if year_cache:
      result.year = year_cache.year

  if len(vin) < 17 or (result.manufacturer is not None and result.model is not None and result.year is not None):
    return result.to_dict()
  
  url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json'
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()

    for item in data['Results']:
      if item['Variable'] == 'Make' and result.manufacturer is not None:
        result.manufacturer = item['Value']
        wmi_cache = Wmi(code=wmi, manufacturer=result.manufacturer)
        db.session.add(wmi_cache)
      elif item['Variable'] == 'Model' and result.model is not None:
        result.model = item['Value']
        vds_cache = Vds(code=vds, model=result.model)
        db.session.add(vds_cache)
      elif item['Variable'] == 'Model Year' and result.year is not None:
        result.year = item['Value']
        year_cache = Year(code=year_code, year=result.year)
        db.session.add(year_cache)
    
    db.session.commit()

  return result.to_dict()