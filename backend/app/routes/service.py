from flask import g, request
from flask_jwt_extended import jwt_required
from app import app
from app import db

from app.routes import COMPANY_PATH_ID, SERVICE_PATH, SERVICE_PATH_ID
from app.models import Company, Service
from app.schemas import BaseResponseSchema, Level
from app.schemas.service import ServiceSchema
from app.services.company import get_company_by_id_check_permission
from app.exceptions import ObjectNotFoundError

@app.route(f'{COMPANY_PATH_ID}{SERVICE_PATH}', methods=['POST'])
@jwt_required()
def create_service(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  data = ServiceSchema().load(request.json)

  check_service = Service.query.filter(Service.company_id == company.id, Service.name.ilike(data['name'])).first()
  if check_service and check_service.id != id:
    return BaseResponseSchema(None, "Service already exists with same name", Level.ERROR).jsonify(), 400

  service = Service(**data)
  service.company = company

  db.session.add(service)
  db.session.commit()
  return BaseResponseSchema(company.to_dict(), "Created succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{SERVICE_PATH}', methods=['GET'])
@jwt_required()
def list_services(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  services = Service.query.filter_by(company_id=company.id).all()
  mapped_services = [service.to_dict() for service in services]
  return BaseResponseSchema(mapped_services).jsonify()

@app.route(f'{COMPANY_PATH_ID}{SERVICE_PATH_ID}', methods=['GET', 'PUT'])
@jwt_required()
def get_service(company_id, service_id):
  company: Company = get_company_by_id_check_permission(company_id)
  service: Service = Service.query.get(service_id)

  if service is None:
    raise ObjectNotFoundError("Service not found")
  
  if service.company_id != company.id:
    raise ObjectNotFoundError("Service not found")

  if request.method == 'GET':
    return BaseResponseSchema(service.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = ServiceSchema().load(request.json, partial=True, unknown='exclude')
    
    check_car: Service = Service.query.filter(Service.company_id == company.id, Service.name.ilike(data['name'])).first()
    if check_car and check_car.id != id:
      return BaseResponseSchema(None, "Service already exists with same vin", Level.ERROR).jsonify(), 400

    service.name = data['name']
    service.price_netto = data['price_netto']
    service.tax = data['tax']
    service.price_brutto = data['price_brutto']
    service.duty = data['duty']
    service.description = data['description']

    db.session.add(service)
    db.session.commit()
    return BaseResponseSchema(service.to_dict(), "Saved succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{SERVICE_PATH_ID}', methods=['DELETE'])
@jwt_required()
def delete_service(company_id, service_id):
  company: Company = get_company_by_id_check_permission(company_id)
  service: Service = Service.query.get(service_id)
  if not service:
    raise ObjectNotFoundError("Service not found")
  
  if service.company_id != company.id:
    raise ObjectNotFoundError("Service not found")
  
  db.session.delete(service)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()

