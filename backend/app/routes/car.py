from flask import g, request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc, func, or_, text
from app import app
from app import db

from app.routes import COMPANY_PATH_ID, CAR_PATH, CAR_PATH_ID
from app.models import Company, Car
from app.schemas import BaseResponseSchema, Level
from app.schemas.car import CarSchema
from app.services.company import get_company_by_id_check_permission
from app.services.car import normalize_plate, vin_decode
from app.exceptions import ObjectNotFoundError

@app.route('/vindecode', methods=['GET'])
@jwt_required()
def vin():
  vin = str(request.args.get('vin', ''))
  if len(vin) < 2:
    return BaseResponseSchema([], "Must be more than two characters", Level.WARNING).jsonify(), 400

  manu_model_year = vin_decode(vin)
  if manu_model_year:
    return BaseResponseSchema(manu_model_year).jsonify()
  else:
    return BaseResponseSchema(None, "Could not decode the VIN number", Level.WARNING).jsonify(), 400

@app.route(f'{COMPANY_PATH_ID}{CAR_PATH}', methods=['POST'])
@jwt_required()
def create_car(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  data = CarSchema().load(request.json)

  plate_normalized = normalize_plate(data['plate'])

  check_company = Car.query.filter(Car.company_id == company.id, Car.plate_normalized.ilike(plate_normalized)).first()
  if check_company and check_company.id != id:
    return BaseResponseSchema(None, "Car already exists with same plate number", Level.ERROR).jsonify(), 400

  car = Car(**data)
  car.company = company

  db.session.add(car)
  db.session.commit()
  return BaseResponseSchema(company.to_dict(), "Created succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{CAR_PATH}', methods=['GET'])
@jwt_required()
def list_cars(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  cars = Car.query.filter_by(company_id=company.id).all()
  mapped_cars = [car.to_dict() for car in cars]
  return BaseResponseSchema(mapped_cars).jsonify()

@app.route(f'{COMPANY_PATH_ID}{CAR_PATH_ID}', methods=['GET', 'PUT'])
@jwt_required()
def get_car(company_id, car_id):
  company: Company = get_company_by_id_check_permission(company_id)
  car: Car = Car.query.get(car_id)

  if car is None:
    raise ObjectNotFoundError("Car not found")
  
  if car.company_id != company.id:
    raise ObjectNotFoundError("Car not found")

  if request.method == 'GET':
    return BaseResponseSchema(car.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = CarSchema().load(request.json, partial=True, unknown='exclude')
    
    check_car: Car = Car.query.filter(Car.company_id == company.id, Car.vin.ilike(data['vin'])).first()
    if check_car and check_car.id != id:
      return BaseResponseSchema(None, "Car already exists with same vin", Level.ERROR).jsonify(), 400

    plate_normalized = normalize_plate(data['plate'])
    check_car: Car = Car.query.filter(Car.company_id == company.id, Car.plate_normalized.ilike(plate_normalized)).first()
    if check_car and check_car.id != id:
      return BaseResponseSchema(None, "Car already exists with same vin", Level.ERROR).jsonify(), 400

    car.vin = data['vin']
    car.model = data['model']
    car.make = data['make']
    car.year = data['year']
    car.plate = data['plate']
    car.plate_normalized = plate_normalized
    car.engine_number = data['engine_number']
    car.engine_code = data['engine_code']
    car.power = data['power']
    
    db.session.add(car)
    db.session.commit()
    return BaseResponseSchema(car.to_dict(), "Saved succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{CAR_PATH_ID}', methods=['DELETE'])
@jwt_required()
def delete_car(company_id, car_id):
  company: Company = get_company_by_id_check_permission(company_id)
  car: Car = Car.query.get(car_id)
  if not car:
    raise ObjectNotFoundError("Car not found")
  
  if car.company_id != company.id:
    raise ObjectNotFoundError("Car not found")
  
  db.session.delete(car)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{CAR_PATH}/search', methods=['GET'])
@jwt_required()
def search(company_id):
  company: Company = get_company_by_id_check_permission(company_id)

  query = str(request.args.get('query', ''))
  if len(query) < 2:
    return BaseResponseSchema([], "Must be more than two characters", Level.WARNING).jsonify(), 400

  #search_query = text("plainto_tsquery('simple', :query)").bindparams(query=query)

  cars = (
    Car.query
    .filter_by(company_id=company.id)
    .filter(
      Car.plate.op('%')(query) |
      Car.vin.op('%')(query) |
      Car.plate.ilike(f'%{query}%') |
      Car.vin.ilike(f'%{query}%')
    )
    .order_by(
        desc(
          func.similarity(Car.plate, query) +
          func.similarity(Car.vin, query)
        )
    )
    .limit(5)
    .all()
  )

  mapped_cars = [car.to_dict() for car in cars]
  return BaseResponseSchema(mapped_cars).jsonify()