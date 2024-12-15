import bcrypt
from flask import g, request
from flask_jwt_extended import jwt_required
from app import app
from app import db

from app.exceptions import ObjectNotFoundError, PermissionDeniedError
from app.models.confirm import Confirm, ConfirmType
from app.routes import COMPANY_PATH, COMPANY_PATH_ID
from app.models import Company, Site, UserSiteUserRole, UserRole
from app.schemas import BaseResponseSchema, Level, CompanySchema
from app.helpers import generate_code
from app.schemas.register import RegisterCompanySchema
from app.services.company import get_user_companies, get_company_by_id_check_permission
from app.services.email import EmailSenderService

@app.route(f'{COMPANY_PATH}', methods=['GET'])
@jwt_required()
def list_company():
  companies = get_user_companies(g.user.id)
  mapped_companies = [company.to_dict() for company in companies]
  return BaseResponseSchema(mapped_companies).jsonify()

@app.route(f'{COMPANY_PATH_ID}', methods=['GET', 'PUT'])
@jwt_required()
def get_company(company_id):
  company: Company = get_company_by_id_check_permission(company_id)

  if request.method == 'GET':
    return BaseResponseSchema(company.to_dict()).jsonify()
  elif request.method == 'PUT':
    data = CompanySchema().load(request.json, partial=True, unknown='exclude')
    
    check_company = Company.query.filter(Company.name.ilike(data['name'])).first()
    if check_company and check_company.id != id:
      return BaseResponseSchema(None, "Company already exists with same name", Level.ERROR).jsonify(), 400

    company.name = data['name']
    company.address = data['address']
    company.email = data['email']
    company.phone_number = data['phone_number']
    company.website = data['website']
    
    db.session.add(company)
    db.session.commit()
    return BaseResponseSchema(company.to_dict(), "Saved succesfully").jsonify()

@app.route(f'{COMPANY_PATH}', methods=['POST'])
def pre_register_company():
  data = RegisterCompanySchema().load(request.json)

  check_confirm = Confirm.query.filter(Confirm.email.ilike(data['email'])).first()
  if check_confirm:
    return BaseResponseSchema("A confirmation email has already been sent", Level.ERROR).jsonify(), 400

  check_confirm = Confirm.query.filter(Confirm.type == ConfirmType.REGISTER_COMPANY, Confirm.name.ilike(data['name'])).first()
  if check_confirm:
    return BaseResponseSchema(None, "Company already exists with same name", Level.ERROR).jsonify(), 400

  check_company = Company.query.filter(Company.name.ilike(data['name'])).first()
  if check_company and check_company.id != id:
    return BaseResponseSchema(None, "Company already exists with same name", Level.ERROR).jsonify(), 400

  password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

  confirm = Confirm(name=data['name'], code=generate_code(code_length=10), type=ConfirmType.REGISTER_COMPANY, email=data['email'], company_name=data['companyName'], user_password=password)
  EmailSenderService.get_instance().send_confirm_emails()

  db.session.add(confirm)
  db.session.commit()
  return BaseResponseSchema("Registration email sent").jsonify()



@app.route(f'{COMPANY_PATH}', methods=['POST'])
@jwt_required()
def create_company():
  data = CompanySchema().load(request.json)
  check_company = Company.query.filter(Company.name.ilike(data['name'])).first()
  if check_company and check_company.id != id:
    return BaseResponseSchema(None, "Company already exists with same name", Level.ERROR).jsonify(), 400

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

@app.route(f'{COMPANY_PATH_ID}', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
  company: Company = Company.query.get(company_id)
  if not company:
    raise ObjectNotFoundError("Company not found")
  
  if company.owner_id != g.user.id:
    raise PermissionDeniedError("You are not allowed to delete this company")

  db.session.delete(company)
  db.session.commit()
  return BaseResponseSchema(None, "Deleted succesfully").jsonify()