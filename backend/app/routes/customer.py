from flask import request
from flask_jwt_extended import jwt_required
from app import app
from app import db

from app.routes import COMPANY_PATH_ID, CUSTOMER_PATH, CUSTOMER_PATH_ID
from app.models import Company, Car, Customer
from app.schemas import BaseResponseSchema, Level
from app.schemas.customer import CustomerSchema
from app.services.company import get_company_by_id_check_permission
from app.exceptions import ObjectNotFoundError

@app.route(f'{COMPANY_PATH_ID}{CUSTOMER_PATH}', methods=['POST'])
@jwt_required()
def create_customer(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  data = CustomerSchema().load(request.json)

  check_customer = Customer.query.filter(Customer.email.ilike(data['email']), Customer.company_id == company.id).first()
  if check_customer and check_customer.id != id:
    return BaseResponseSchema(None, "Customer already exists with same email", level=Level.ERROR).jsonify(), 400

  customer = Customer(**data)
  customer.company = company

  db.session.add(customer)
  db.session.commit()
  return BaseResponseSchema(customer.to_dict(), "Created succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{CUSTOMER_PATH}', methods=['GET'])
@jwt_required()
def list_customers(company_id):
  company: Company = get_company_by_id_check_permission(company_id)
  customers = Customer.query.filter_by(company_id=company.id).all()
  mapped_cars = [customer.to_dict() for customer in customers]
  return BaseResponseSchema(mapped_cars).jsonify()

@app.route(f'{COMPANY_PATH_ID}{CUSTOMER_PATH_ID}', methods=['GET', 'PUT'])
@jwt_required()
def get_customer(company_id, customer_id):
  company: Company = get_company_by_id_check_permission(company_id)
  customer: Customer = Customer.query.get(customer_id)

  if customer is None:
    raise ObjectNotFoundError("Customer not found")
  
  if customer.company_id != company.id:
    raise ObjectNotFoundError("Customer not found")

  if request.method == 'GET':
    return BaseResponseSchema(customer.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = CustomerSchema().load(request.json, partial=True, unknown='exclude')
    
    check_customer: Customer = Customer.query.filter(Customer.company ,Customer.email.ilike(data['email'])).first()
    if check_customer and check_customer.id != id:
      return BaseResponseSchema(None, "Customer already exists with same email", level=Level.ERROR).jsonify(), 400

    check_customer: Customer = Customer.query.filter(Customer.phone.ilike(data['phone'])).first()
    if check_customer and check_customer.id != id:
      return BaseResponseSchema(None, "Customer already exists with same phone", level=Level.ERROR).jsonify(), 400

    customer.name = data['name']
    customer.email = data['email']
    customer.phone = data['phone']
    customer.address = data['address']
    customer.comment = data['comment']
    
    db.session.add(customer)
    db.session.commit()
    return BaseResponseSchema(company.to_dict(), "Saved succesfully").jsonify()

@app.route(f'{COMPANY_PATH_ID}{CUSTOMER_PATH_ID}', methods=['DELETE'])
@jwt_required()
def delete_customer(company_id, customer_id):
  company: Company = get_company_by_id_check_permission(company_id)
  customer: Customer = Customer.query.get(customer_id)
  if not customer:
    raise ObjectNotFoundError("Customer not found")
  
  if customer.company_id != company.id:
    raise ObjectNotFoundError("Customer not found")
  
  db.session.delete(customer)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()

