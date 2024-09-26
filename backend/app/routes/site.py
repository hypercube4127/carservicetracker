from app.schemas import BaseResponseSchema
from flask import request
from app.models import Site
from app import app, db

@app.route('/company/<int:company_id>/sites', methods=['GET'])
def get_sites(company_id):
  sites = Site.query.filter_by(company_id=company_id).all()
  mapped_sites = [site.to_dict() for site in sites]
  return BaseResponseSchema().jsonify(sites)

@app.route('/company/<int:company_id>/sites/<int:site_id>', methods=['GET'])
def get_site(company_id, site_id):
  site = Site.query.filter_by(company_id=company_id, id=site_id).first()
  return BaseResponseSchema().jsonify(site)

@app.route('/company/<int:company_id>/sites', methods=['POST'])
def create_site(company_id):
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