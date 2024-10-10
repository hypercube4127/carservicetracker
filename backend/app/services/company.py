from app.models.company import Company
from app.models.user import User
from app.models.user_site_role import UserSiteUserRole

def get_user_companies(user_id):
  user: User = User.query.get(user_id)
  if user.is_admin():
    return Company.query.all()
  companies = set()
  owned_companies = Company.query.filter_by(owner_id=user.id).all()
  for company in owned_companies:
    companies.add(company)

  sites = UserSiteUserRole.query.filter_by(user_id=user.id).all()
  for site in sites:
    company = Company.query.get(site.site.company_id)
    if company not in companies:
      companies.add(company)
  return companies

def get_user_companies_ids( user_id):
  companies = get_user_companies(user_id)
  return [company.id for company in companies]
