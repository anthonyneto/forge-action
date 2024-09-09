from manage_functions import *
from manage_rds import *
from manage_mysql import *
from manage_site import *

BRANCH_NAME       = os.getenv('GITHUB_BRANCH_NAME', 'dev')

# RDS_ROOT_USERNAME = os.getenv('RDS_ROOT_USERNAME')
# RDS_ROOT_PASSWORD = os.getenv('RDS_ROOT_PASSWORD')
# RDS_NAME          = os.getenv('CUSTOM_RDS_NAME', 'staging') # this needs to be fixed so the default is from a function not a static string.
# RDS_PR_DB_NAME    = os.getenv('CUSTOM_RDS_PR_NAME', get_rds_pr_db_name())

FORGE_API_TOKEN = os.getenv('FORGE_API_TOKEN')
FORGE_SERVER_ID = os.getenv('FORGE_SERVER_ID')
FORGE_ZONE      = os.getenv('FORGE_ZONE')
FORGE_GIT_URL   = os.getenv('FORGE_GIT_URL')
FORGE_DOMAIN    = os.getenv('FORGE_DOMAIN', DEFAULT_SITE_DOMAIN(BRANCH_NAME, FORGE_ZONE))
FORGE_DIRECTORY = os.getenv('FORGE_SITE_DIRECTORY', DEFAULT_SITE_DIRECTORY(BRANCH_NAME, FORGE_ZONE))

# create_rds_instance(
#   db_instance_id=RDS_NAME,
#   master_username=RDS_ROOT_USERNAME,
#   master_password=RDS_ROOT_PASSWORD,
#   vpc_id='vpc-0e7cfb09a583f844e',
#   db_subnet_group_name='rds-public'
# )

# wait_for_db_instance_available(RDS_NAME)

# RDS_HOST = get_rds_endpoint(RDS_NAME)
# print(f"RDS instance public endpoint: {RDS_HOST}")

# create_database_and_user(
#   host=RDS_HOST,
#   user=RDS_ROOT_USERNAME,
#   password=RDS_ROOT_PASSWORD,
#   new_db_name=RDS_PR_DB_NAME,
#   new_user=RDS_PR_DB_NAME,
#   new_user_password=RDS_PR_DB_NAME
# )

for key, value in os.environ.items():
    print(f"{key}: {value}")

print(BRANCH_NAME)
print(FORGE_SERVER_ID)
print(FORGE_ZONE)
print(FORGE_GIT_URL)

# forge_manage_site(
#   api_token=FORGE_API_TOKEN,
#   branch=BRANCH_NAME,
#   git_url=FORGE_GIT_URL,
#   server_id=FORGE_SERVER_ID,
#   domain=FORGE_DOMAIN,
#   directory=FORGE_DIRECTORY
# )
