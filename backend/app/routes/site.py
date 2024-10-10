from app.models.company import Company
from app.models.user_site_role import UserSiteUserRole
from app.schemas import BaseResponseSchema, Level
from flask import request, g
from app.models import Site
from app import app, db

@app.route('/company/<int:company_id>/sites', methods=['GET'])
def get_sites(company_id):
  company = Company.query.get(company_id)

  if company is None:
    return BaseResponseSchema(None, "Unauthorized", level=Level.ERROR).jsonify(), 400

  if g.is_admin is False and company.owner_id != g.user.id:
    user_roles = UserSiteUserRole.query.filter_by(user_id=g.user.id).all()
    site_ids = [role.site_id for role in user_roles]
    sites = Site.query.filter(Site.company_id == company.id & Site.id.in_(site_ids)).all()
    if len(sites) == 0:
      return BaseResponseSchema(None, "Unauthorized", level=Level.ERROR).jsonify, 400
  else:
    sites = Site.query.filter_by(company=company).all()

  mapped_sites = [site.to_dict() for site in sites]
  return BaseResponseSchema(mapped_sites).jsonify()

@app.route('/company/<int:company_id>/sites/<int:site_id>', methods=['GET'])
def get_site(company_id, site_id):
  company = Company.query.get(company_id)
  if company is None:
    return BaseResponseSchema("Unauthorized", level=Level.ERROR).jsonify(), 400

  site = Site.query.filter_by(company=company, id=site_id).first()
  if site is None:
    return BaseResponseSchema("Unauthorized", level=Level.ERROR).jsonify(), 400

  if company.owner_id == g.user.id or UserSiteUserRole.query.filter_by(user=g.user, site=site).first():
    return BaseResponseSchema(site.to_dict()).jsonify()

  return BaseResponseSchema("Unauthorized", level=Level.ERROR).jsonify(), 400

@app.route('/company/<int:company_id>/sites', methods=['POST'])
def create_site(company_id):
  company = Company.query.get(company_id)

  if company is None:
    return BaseResponseSchema(None, "Unauthorized", level=Level.ERROR).jsonify(), 400

  data = request.json
  site = Site(**data, company_id=company_id)
  db.session.add(site)
  db.session.commit()
  return BaseResponseSchema().jsonify(site)

@app.route('/company/<int:company_id>/sites/<int:site_id>', methods=['PUT'])
def update_site(company_id, site_id):
  data = request.json
  site = Site.query.filter_by(company_id=company_id, id=site_id).first()
  site.update(**data)
  db.session.commit()
  return BaseResponseSchema().jsonify(site)