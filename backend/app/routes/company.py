from flask import g, request
from flask_jwt_extended import jwt_required
from app import app
from app import db

from app.models import Company, Site, UserSiteUserRole, UserRole
from app.schemas import BaseResponseSchema, Level, CompanySchema
from app.helpers import generate_code
from app.services import company

@app.route('/company', methods=['GET'])
@jwt_required()
def list_company():
  companies = company.get_user_companies(g.user.id)
  mapped_companies = [company.to_dict() for company in companies]
  return BaseResponseSchema(mapped_companies).jsonify()

@app.route('/company/<int:id>', methods=['GET', 'PUT'])
@jwt_required()
def get_company(id):
  company: Company = Company.query.get(id)

  if company is None:
    return BaseResponseSchema(None, "Unauthorized", level=Level.ERROR).jsonify(), 400
  
  if g.is_admin is False and company.owner_id != g.user.id:
    user_roles = UserSiteUserRole.query.filter_by(user_id=g.user.id).all()
    company_ids = [role.site.company_id for role in user_roles]
    if company.id not in company_ids:
      return BaseResponseSchema(None, "Unauthorized", level=Level.ERROR).jsonify

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
@jwt_required()
def create_company():
  data = CompanySchema().load(request.json)
  if Company.query.filter_by(name=data['name']).first():
    return BaseResponseSchema("Company already exists", Level.ERROR).jsonify()

  data['code'] = generate_code()
  data['owner_id'] = g.user.id
  company = Company(**data)
  
  default_site: Site = Site(name=f"{company.name} first site", company=company)
  site_role = UserSiteUserRole(user=g.user, site=default_site, role=UserRole.ADMIN)

  db.session.add(company)
  db.session.add(default_site)
  db.session.add(site_role)
  db.session.commit()
  return BaseResponseSchema(company.to_dict(), "Created succesfully").jsonify()

@app.route('/company/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
  company = Company.query.get(id)
  db.session.delete(company)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()