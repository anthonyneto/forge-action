import json
import re
import os
import time
import requests

def handle_request_error(e, action):
  if e.response is not None:
    try:
      error_details = e.response.json()
      print(f"Error during {action}: {e}")
      print("Error details:", error_details)
    except ValueError:
      print(f"Error during {action}: {e}")
      print("Error response is not valid JSON:", e.response.text)
  else:
    print(f"Error during {action}: {e}")

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

def deploy_now(api_token, server_id, site_name):
  site_id = get_site_id(api_token, server_id, site_name)
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/deployment/deploy'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }

  try:
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    print("Deployment triggered successfully.")
    return response.json()
  except requests.RequestException as e:
    handle_request_error(e, "triggering deployment")
    return None

def get_sites(api_token, server_id):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites'
  headers = {'Authorization': f'Bearer {api_token}'}
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('sites', [])
  except requests.RequestException as e:
    handle_request_error(e, "fetching sites")
    return []

def check_site_status(api_token, server_id, site_id, timeout=300):
  start_time = time.time()

  while True:
    site_details = get_sites(api_token, server_id)

    if isinstance(site_details, list):
      site_data = next((site for site in site_details if site['id'] == site_id), None)
      if site_data:
        if site_data['status'] == 'installed':
          return site_data
        else:
          print("Site is not installed yet, checking again in 15 seconds...")
      else:
        print("Site data not found.")
    else:
      print("Failed to retrieve site details.")
      return None

    if time.time() - start_time > timeout:
      print("Timeout reached while waiting for site to install.")
      return None

    time.sleep(15)
