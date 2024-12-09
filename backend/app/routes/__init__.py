
COMPANY_PATH = '/company'
CAR_PATH = '/car'
USER_PATH = '/user'
SITE_PATH = '/site'
AUTH_PATH = '/auth'
CONFIRM_PATH = '/confirm'
CUSTOMER_PATH = '/customer'
INVALIDATED_TOKEN_PATH = '/invalidated_token'
USER_SITE_ROLE_PATH = '/user_site_role'
SERVICE_PATH = '/service'

COMPANY_PARAM = '/<int:company_id>'
CUSTOMER_PARAM = '/<int:customer_id>'
CAR_PARAM = '/<int:car_id>'
USER_PARAM = '/<int:user_id>'
SITE_PARAM = '/<int:site_id>'
INVALIDATED_TOKEN_PARAM = '/<int:invalidated_token_id>'
USER_SITE_ROLE_PARAM = '/<int:user_site_role_id>'
SERVICE_PARAM = '/<int:service_id>'

COMPANY_PATH_ID = f'{COMPANY_PATH}{COMPANY_PARAM}'
CAR_PATH_ID = f'{CAR_PATH}{CAR_PARAM}'
USER_PATH_ID = f'{USER_PATH}{USER_PARAM}'
SITE_PATH_ID = f'{SITE_PATH}{SITE_PARAM}'
CUSTOMER_PATH_ID = f'{CUSTOMER_PATH}{CUSTOMER_PARAM}'
SERVICE_PATH_ID = f'{SERVICE_PATH}{SERVICE_PARAM}'

from .main import *
from .auth import *
from .user import *
from .company import *
from .site import *
from .car import *
from .confirm import *