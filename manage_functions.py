import json
import re
import os
import requests

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

def get_site_id(api_token, server_id, site_name):
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites"
  headers = {'Authorization': f'Bearer {api_token}'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_dict = json.loads(response.text)

    for site in response_dict['sites']:
      if site['name'] == site_name:
        return site['id']

  except requests.exceptions.HTTPError as err:
      print(f"HTTP error occurred: {err}")
  except Exception as err:
      print(f"An error occurred: {err}")
