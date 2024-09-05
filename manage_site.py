import os
import requests

from manage_functions import get_github_branch_name

DEFAULT_ZONE = 'example.com'
DEFAULT_PHP_VERSION = 'php82'
DEFAULT_PROJECT_TYPE = 'php'
DEFAULT_GIT_PROVIDER = 'github'
DEFAULT_GIT_BRANCH = 'dev'
DEFAULT_GIT_URL = 'bizhaven1/wapp'

def get_default_site_domain():
  zone = os.getenv('ZONE', DEFAULT_ZONE)
  branch_name = get_github_branch_name() or 'unset'
  return f'api.{branch_name}.app.{zone}'

def get_default_site_directory():
  return f"/home/forge/{get_default_site_domain()}/public"

def get_sites(api_token, server_id):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites'
  headers = {'Authorization': f'Bearer {api_token}'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    sites_data = response.json()
    return sites_data.get('sites', [])
  except requests.RequestException as e:
    print(f"Error fetching sites: {e}")
    return []

def get_deployment_history(api_token, server_id, site_id):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/deployment-history'
  headers = {'Authorization': f'Bearer {api_token}'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('deployments', [])
  except requests.RequestException as e:
    print(f"Error fetching deployments: {e}")
    return []

def create_site(api_token, server_id, domain, directory, database, php_version=DEFAULT_PHP_VERSION, project_type=DEFAULT_PROJECT_TYPE, username='forge'):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }
  payload = {
    "domain": domain,
    "project_type": project_type,
    "directory": directory,
    "username": username,
    "database": database,
    "php_version": php_version
  }

  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    if 'data' in response_json:
      return response_json
    else:
      print("Unexpected response structure:", response_json)
      return None
  except requests.RequestException as e:
    print(f"Error creating site: {e}")
    return None


def create_deployment_git(api_token, server_id, site_id, git_url=DEFAULT_GIT_URL, git_provider=DEFAULT_GIT_PROVIDER, git_branch=DEFAULT_GIT_BRANCH):
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/git'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }
  payload = {
    'provider': git_provider,
    'repository': git_url,
    'branch': git_branch
  }

  print(payload)

  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    print("Deployment created successfully.")
    return response_json
  except requests.RequestException as e:
    # Log detailed error response
    if e.response is not None:
      try:
        error_details = e.response.json()
        print(f"Error creating deployment: {e}")
        print("Error details:", error_details)
      except ValueError:
        print(f"Error creating deployment: {e}")
        print("Error response is not valid JSON:", e.response.text)
    else:
      print(f"Error creating deployment: {e}")
    return None


def handle_response(response):
  if response is not None:
    if response.get('status_code', 200) == 200:
      print("Operation successful!")
    else:
      print(f"Failed to perform operation: {response.get('status_code', 'Unknown')}")
      try:
        error_details = response.json()
        print("Error details:", error_details)
      except ValueError:
        print("Error response is not valid JSON:", response.text)
  else:
    print("No response received.")

def forge_manage_site(branch, database=''):
  api_token = os.getenv('FORGE_API_TOKEN')
  server_id = os.getenv('FORGE_SERVER_ID')
  domain = os.getenv('FORGE_SITE', get_default_site_domain())
  directory = os.getenv('FORGE_DIRECTORY', get_default_site_directory())

  # Retrieve list of sites
  sites = get_sites(api_token, server_id)
  if not isinstance(sites, list):
    print("Failed to retrieve sites.")
    return

  # Check if the site already exists
  site_data = next((site for site in sites if site.get('name') == domain), None)

  if site_data:
    site_id = site_data['id']
    print(f"Site '{domain}' already exists.")

    # Check if the deployment already exists
    deployments = get_deployment_history(api_token, server_id, site_id)
    deployment_exists = any(d['repository'] == DEFAULT_GIT_URL and d['branch'] == branch for d in deployments)

    if deployment_exists:
      print(f"Deployment for {DEFAULT_GIT_URL} on branch {branch} already exists.")
    else:
      # Create deployment if it doesn't exist
      response = create_deployment_git(api_token, server_id, site_id, git_branch=branch)
      handle_response(response)
  else:
    # Create site if it doesn't exist
    response = create_site(api_token, server_id, domain, directory, database)
    if response and 'data' in response:
      site_id = response['data']['id']
      # Create deployment for the new site
      response = create_deployment_git(api_token, server_id, site_id, git_branch=branch)
      handle_response(response)
    else:
      print("Failed to create site, cannot set up deployment.")
