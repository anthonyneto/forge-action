import requests

DEFAULT_PHP_VERSION = 'php82'
DEFAULT_PROJECT_TYPE = 'php'
DEFAULT_GIT_PROVIDER = 'github'

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
    print("Deployment created successfully.")
    return response_json
  except requests.RequestException as e:
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

def forge_manage_site(api_token, domain, directory, server_id, branch, git_url, database=''):
  sites = get_sites(api_token, server_id)
  if not isinstance(sites, list):
    print("Failed to retrieve sites.")
    return

  print(sites)
  print(domain)
  exit(0)

  site_data = next((site for site in sites if site.get('name') == domain), None)

  if site_data:
    site_id = site_data['id']
    print(f"Site '{domain}' already exists.")

    deployments = get_deployment_history(api_token, server_id, site_id)
    deployment_exists = any(d['repository'] == git_url and d['branch'] == branch for d in deployments)

    if deployment_exists:
      print(f"Deployment for {git_url} on branch {branch} already exists.")
    else:
      create_deployment_git(api_token, server_id, site_id, branch, git_url)
  else:
    response = create_site(api_token, server_id, domain, directory, database)
    if response and 'data' in response:
      site_id = response['data']['id']
      create_deployment_git(api_token, server_id, site_id, branch, git_url)
    else:
      print("Failed to create site, cannot set up deployment.")
