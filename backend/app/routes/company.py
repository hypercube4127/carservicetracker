import random
import string

from flask import g, request
from app import app
from app import db

from app.models import Company
from app.schemas import BaseResponseSchema, Level, CompanySchema
from app.helpers import generate_code

@app.route('/company', methods=['GET'])
def list_company():
  companies = Company.query.all()
  mapped_companies = [company.to_dict() for company in companies]
  return BaseResponseSchema(mapped_companies).jsonify()

@app.route('/company/<int:id>', methods=['GET', 'PUT'])
def get_company(id):
  company: Company = Company.query.get(id)
  if request.method == 'GET':
    return BaseResponseSchema(company.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = CompanySchema().load(request.json, partial=True, unknown='exclude')
    
    company.name = data['name']
    company.address = data['address']
    company.email = data['email']
    company.phone_number = data['phone_number']
    company.website = data['website']
    
    db.session.commit()
    return BaseResponseSchema(company.to_dict(), "Saved succesfully").jsonify()
  
@app.route('/company', methods=['POST'])
def create_company():
  data = CompanySchema().load(request.json)
  if Company.query.filter_by(name=data['name']).first():
    return BaseResponseSchema(None, "Company already exists", level=Level.ERROR).jsonify()

 
  data['code'] = generate_code()
  data['owner_id'] = g.user.id
  company = Company(**data)
  
  db.session.add(company)
  db.session.commit()
  return BaseResponseSchema(company.to_dict(), "Created succesfully").jsonify()

@app.route('/company/<int:id>', methods=['DELETE'])
def delete_company(id):
  company = Company.query.get(id)
  db.session.delete(company)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()