from app.models.user import User
from app.models.user_site_role import UserSiteUserRole

def get_user_relations(user_id):
  user: User = User.query.get(user_id)
  if user.is_admin():
    return User.query.all()
  
  users = set()
  users.add(user)
  sites = UserSiteUserRole.query.filter_by(user_id=user.id).all()
  for site in sites:
    users_in_site = UserSiteUserRole.query.filter_by(site_id=site.site_id).all()
    for user_site_role in users_in_site:
      users.add(user_site_role.user)
  return users

def get_user_relations_ids(user_id):
  users = get_user_relations(user_id)
  return [user.id for user in users]