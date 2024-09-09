import os
import boto3
from botocore.exceptions import ClientError

AWS_REGION            = os.getenv('INPUT_AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID     = os.getenv('INPUT_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('INPUT_AWS_SECRET_ACCESS_KEY')

session = boto3.Session(
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
  region_name=AWS_REGION
)

ec2_client = session.client('ec2')
rds_client = session.client('rds')

def create_or_update_security_group(
  group_name,
  description,
  vpc_id
):
  try:
    response = ec2_client.describe_security_groups(Filters=[
      {
        'Name': 'group-name',
        'Values': [group_name]
      }
    ])

    if response['SecurityGroups']:
      security_group_id = response['SecurityGroups'][0]['GroupId']
      print(f"Security group {group_name} already exists with ID {security_group_id}")

      existing_rules = response['SecurityGroups'][0].get('IpPermissions', [])
      rule_exists = any(
        rule for rule in existing_rules
        if rule['IpProtocol'] == 'tcp' and
           rule['FromPort'] == 3306 and
           rule['ToPort'] == 3306 and
           any(ip_range['CidrIp'] == '0.0.0.0/0' for ip_range in rule.get('IpRanges', []))
      )

      if not rule_exists:
        ec2_client.authorize_security_group_ingress(
          GroupId=security_group_id,
          IpPermissions=[
            {
              'IpProtocol': 'tcp',
              'FromPort': 3306,
              'ToPort': 3306,
              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
          ]
        )
        print(f"Updated inbound rules for existing security group {group_name}")
      return security_group_id

  except ClientError as e:
    print(f"Error describing security groups: {e}")
    raise

  try:
    print(f"Creating security group {group_name}")
    response = ec2_client.create_security_group(
      GroupName=group_name,
      Description=description,
      VpcId=vpc_id
    )
    security_group_id = response['GroupId']
    print(f"Created security group {group_name} with ID {security_group_id}")

    ec2_client.authorize_security_group_ingress(
      GroupId=security_group_id,
      IpPermissions=[
        {
          'IpProtocol': 'tcp',
          'FromPort': 3306,
          'ToPort': 3306,
          'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
      ]
    )
    print(f"Configured inbound rules for new security group {group_name}")
    return security_group_id

  except ClientError as e:
    print(f"Error creating security group {group_name}: {e}")
    raise

def create_rds_instance(
  db_instance_id,
  master_username,
  master_password,
  vpc_id,
  db_instance_class='db.t4g.micro',
  engine='mysql',
  allocated_storage=20,
  backup_retention_period=0,
  db_subnet_group_name=None
):

  security_group_id = create_or_update_security_group(
    group_name=db_instance_id,
    description=f'Security group for RDS: {db_instance_id}',
    vpc_id=vpc_id
  )

  try:
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    print(f"RDS instance {db_instance_id} already exists.")
    return response

  except ClientError as e:
    if e.response['Error']['Code'] == 'DBInstanceNotFound':
      print(f"Creating RDS instance {db_instance_id}...")
      response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_instance_id,
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        DBInstanceClass=db_instance_class,
        Engine=engine,
        AllocatedStorage=allocated_storage,
        BackupRetentionPeriod=backup_retention_period,
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName=db_subnet_group_name,
        PubliclyAccessible=True
      )
      print(f"RDS instance {db_instance_id} creation initiated.")
      return response
    else:
      raise

def delete_rds_instance(db_instance_id, skip_final_snapshot=True):
  try:
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    print(f"Deleting RDS instance {db_instance_id}...")
    rds_client.delete_db_instance(
      DBInstanceIdentifier=db_instance_id,
      SkipFinalSnapshot=skip_final_snapshot
    )
    print(f"RDS instance {db_instance_id} deletion initiated.")
    return response

  except ClientError as e:
    if e.response['Error']['Code'] == 'DBInstanceNotFound':
      print(f"RDS instance {db_instance_id} does not exist.")
    else:
      raise

def wait_for_db_instance_available(db_instance_id, timeout=300):
  print(f"Waiting for RDS instance {db_instance_id} to be available with a timeout of {timeout} seconds...")
  try:
    waiter = rds_client.get_waiter('db_instance_available')
    waiter.wait(
      DBInstanceIdentifier=db_instance_id,
      WaiterConfig={
        'Delay': 30,
        'MaxAttempts': timeout // 30
      }
    )
    print(f"RDS instance {db_instance_id} is now available.")
  except ClientError as e:
    print(f"Error while waiting for RDS instance {db_instance_id}: {e}")
    raise
  except Exception as e:
    print(f"Timeout occurred while waiting for RDS instance {db_instance_id}: {e}")
    raise

def get_rds_endpoint(db_instance_id):
  try:
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    endpoint = response['DBInstances'][0]['Endpoint']['Address']
    return f"{endpoint}"
  except ClientError as e:
    print(f"Error retrieving endpoint for RDS instance {db_instance_id}: {e}")
    raise
