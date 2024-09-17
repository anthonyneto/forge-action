import os
import re

def to_web_safe_string(string):
  string = string.lower()
  string = re.sub(r'[^a-z0-9-]', '-', string)
  string = string.strip('-')

  labels = string.split('.')
  labels = [label[:63] for label in labels]
  string = '.'.join(labels)

  return string

def to_mysql_safe_string(string):
    string = string.lower()
    string = re.sub(r'[^a-z0-9_]', '_', string)
    string = re.sub(r'_{2,}', '_', string)
    string = string.strip('_')

    if len(string) > 64:
        string = string[:64]

    return string

def get_rds_pr_db_name(branch):
  rds_pr_db_name = to_mysql_safe_string(branch)
  return rds_pr_db_name

def DEFAULT_SITE_DOMAIN(branch, zone):
  branch = to_web_safe_string(branch)
  return f'{branch}.api.app.{zone}'

def DEFAULT_SITE_DIRECTORY(branch, zone):
  return f"/home/forge/{DEFAULT_SITE_DOMAIN(branch, zone)}/public"
