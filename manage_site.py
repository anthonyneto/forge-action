import time
import json
import requests
from manage_functions import *

DEFAULT_USERNAME = 'forge'
DEFAULT_PHP_VERSION = 'php82'
DEFAULT_PROJECT_TYPE = 'php'
DEFAULT_GIT_PROVIDER = 'github'

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

def get_repository_status(api_token, server_id, site_id):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}'
  headers = {'Authorization': f'Bearer {api_token}'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_dict = json.loads(response.text)
    return response_dict['site']['repository_status']

  except requests.exceptions.HTTPError as err:
      print(f"HTTP error occurred: {err}")
  except Exception as err:
      print(f"An error occurred: {err}")

def create_site(api_token, server_id, domain, directory, database, php_version=DEFAULT_PHP_VERSION, project_type=DEFAULT_PROJECT_TYPE, username=DEFAULT_USERNAME):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }
  payload = {
    "domain": domain,
    "project_type": project_type,
    "directory": "/public",
    "web_directory": directory,
    "username": username,
    "database": database,
    "php_version": php_version
  }
  print(payload)
  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
  except requests.RequestException as e:
    handle_request_error(e, "creating site")
    return None

def create_deployment_git(api_token, server_id, site_id, branch, git_url, git_provider=DEFAULT_GIT_PROVIDER):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/git'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }
  payload = {
    'provider': git_provider,
    'repository': git_url,
    'branch': branch
  }

  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    if 'site' in response_json:
      print("Deployment created")
      return response_json
    else:
      print("Unexpected response structure from create_deployment_git:", response_json)
      return None

  except requests.RequestException as e:
    handle_request_error(e, "creating deployment")
    return None

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
          print("Site is not installed yet, checking again in 5 seconds...")
      else:
        print("Site data not found.")
    else:
      print("Failed to retrieve site details.")
      return None

    if time.time() - start_time > timeout:
      print("Timeout reached while waiting for site to install.")
      return None

    time.sleep(5)

def forge_manage_site(api_token, domain, directory, server_id, branch, git_url, database=''):
  sites = get_sites(api_token, server_id)
  if not isinstance(sites, list):
    print("Failed to retrieve sites.")
    return

  site_data = next((site for site in sites if site.get('name') == domain), None)

  if site_data:
    site_id = site_data['id']
    print(f"Site '{domain}' already exists.")
  else:
    response = create_site(api_token, server_id, domain, directory, database)
    if response:
      site_id = response['site']['id']
      print(f"Waiting for site installation to complete for site id: {site_id}")
      site_data = check_site_status(api_token, server_id, site_id)
      if not site_data:
        print("Failed to confirm site status after creation.")
        return
    else:
      print("Failed to create site, cannot set up deployment.")
      return

  if get_repository_status(api_token, server_id, site_id) == 'installed':
    print(f"Repository already setup for {git_url}")
  else:
    create_deployment_git(api_token, server_id, site_id, branch, git_url)
