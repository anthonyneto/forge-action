from manage_functions import *
from manage_rds import create_rds_instance, wait_for_db_instance_available, get_rds_endpoint
from manage_mysql import create_database_and_user
from manage_site import forge_manage_site
from manage_site_env import forge_manage_site_env

BRANCH_NAME = os.getenv('INPUT_GITHUB_BRANCH_NAME', 'dev')

RDS_VPC_ID        = os.getenv('INPUT_RDS_VPC_ID')
RDS_SUBNET_GROUP  = os.getenv('INPUT_RDS_SUBNET_GROUP')
RDS_ROOT_USERNAME = os.getenv('INPUT_RDS_ROOT_USERNAME')
RDS_ROOT_PASSWORD = os.getenv('INPUT_RDS_ROOT_PASSWORD')
RDS_NAME          = os.getenv('INPUT_RDS_NAME', 'staging') # this needs to be fixed so the default is from a function not a static string.
RDS_PR_DB_NAME    = os.getenv('INPUT_RDS_PR_NAME', get_rds_pr_db_name(BRANCH_NAME))

FORGE_API_TOKEN = os.getenv('INPUT_FORGE_API_TOKEN')
FORGE_SERVER_ID = os.getenv('INPUT_FORGE_SERVER_ID')
FORGE_ZONE      = os.getenv('INPUT_FORGE_ZONE')
FORGE_GIT_URL   = os.getenv('INPUT_FORGE_GIT_URL')
FORGE_DOMAIN    = os.getenv('INPUT_FORGE_DOMAIN', DEFAULT_SITE_DOMAIN(BRANCH_NAME, FORGE_ZONE))
FORGE_DIRECTORY = os.getenv('INPUT_FORGE_SITE_DIRECTORY', DEFAULT_SITE_DIRECTORY(BRANCH_NAME, FORGE_ZONE))

create_rds_instance(
  db_instance_id=RDS_NAME,
  master_username=RDS_ROOT_USERNAME,
  master_password=RDS_ROOT_PASSWORD,
  vpc_id=RDS_VPC_ID,
  db_subnet_group_name=RDS_SUBNET_GROUP
)

wait_for_db_instance_available(RDS_NAME)

RDS_HOST = get_rds_endpoint(RDS_NAME)
print(f"RDS instance public endpoint: {RDS_HOST}")

create_database_and_user(
  host=RDS_HOST,
  user=RDS_ROOT_USERNAME,
  password=RDS_ROOT_PASSWORD,
  new_db_name=RDS_PR_DB_NAME,
  new_user=RDS_PR_DB_NAME,
  new_user_password=RDS_PR_DB_NAME
)

forge_manage_site(
  api_token=FORGE_API_TOKEN,
  branch=BRANCH_NAME,
  git_url=FORGE_GIT_URL,
  server_id=FORGE_SERVER_ID,
  domain=FORGE_DOMAIN,
  directory=FORGE_DIRECTORY
)

FORGE_ENV_OVERRIDES = {
  "APP_URL": f"https://{FORGE_DOMAIN}",
  "DB_HOST": RDS_HOST,
  "DB_DATABASE": RDS_PR_DB_NAME,
  "DB_USERNAME": RDS_PR_DB_NAME,
  "DB_PASSWORD": RDS_PR_DB_NAME
}

forge_manage_site_env(
  api_token=FORGE_API_TOKEN,
  server_id=FORGE_SERVER_ID,
  site_name=FORGE_DOMAIN,
  overrides=FORGE_ENV_OVERRIDES
)
