from manage_functions import *
from manage_rds import *
from manage_mysql import *
from manage_site import *

BRANCH_NAME       = os.getenv('GITHUB_BRANCH_NAME', 'dev')
SAFE_BRANCH_NAME  = os.getenv('FORGE_SITE', get_github_branch_name())
RDS_ROOT_USERNAME = os.getenv('MYSQL_ROOT_USERNAME', 'admin')
RDS_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'admin')
RDS_NAME          = os.getenv('CUSTOM_RDS_NAME', 'staging') # this needs to be fixed so the default is from a function not a static string.
RDS_PR_DB_NAME    = os.getenv('CUSTOM_RDS_PR_NAME', get_rds_pr_db_name())

# print(RDS_NAME)
# print(RDS_PR_DB_NAME)
# print(os.getenv('MYSQL_ROOT_USERNAME'))

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

# forge_manage_site(BRANCH_NAME)

hello_world()
