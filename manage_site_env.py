import json
import requests
import os

def get_site_id(api_token, server_id, site_name):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN')
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites"
  headers = {
    "Authorization": f"Bearer {FORGE_TOKEN}"
  }

  print(site_name)
  exit()

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_dict = json.loads(response.text)
    print(response.text)

    for site in response_dict['sites']:
      if site['name'] == site_name:
        return site['id']

  except requests.exceptions.HTTPError as err:
      print(f"HTTP error occurred: {err}")
  except Exception as err:
      print(f"An error occurred: {err}")

def get_environment_variables(server_id, site_id):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN')
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/env"

  headers = {
    "Authorization": f"Bearer {FORGE_TOKEN}"
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
  except Exception as err:
    print(f"An error occurred: {err}")

def update_environment_variables(server_id, site_id, content, overrides):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN')
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/env"

  headers = {
    "Authorization": f"Bearer {FORGE_TOKEN}",
    "Content-Type": "application/json"
  }

  # turn content into a dict to make it easier to update values
  content_dict = {}
  for line in content.strip().split('\n'):
    line = line.strip()
    if line.startswith("#"):
      continue
    if '=' in line:
        key, value = line.split('=', 1)
        content_dict[key] = value.strip('"')

  # turn content dict back into .env format for POST
  content_env = []
  for key, value in content_dict.items():
      if key in overrides:
        value = overrides[key]
      content_env.append(f"{key}={value}")
  updated_payload = "\n".join(content_env)

  payload = {
    "content": updated_payload
  }

  try:
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.text
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred while updating environment variables: {err}")
  except Exception as err:
    print(f"An error occurred while updating environment variables: {err}")

def forge_manage_site_env(api_token, server_id, site_name, overrides):
  print('Updating .env')
  site_id = get_site_id(api_token, server_id, site_name)
  print(site_id)
  current_environment_variables = get_environment_variables(server_id, site_id)
  print(current_environment_variables)
  print(overrides)
  update_environment_variables(server_id, site_id, current_environment_variables, overrides)

# FORGE_ENV_OVERRIDES = {
#   "APP_URL": "https://ci-pr-environments.api.app.bizhaven.com",
#   "DB_HOST": "staging.ckaqvri2ycor.us-west-2.rds.amazonaws.com"
# }

# forge_manage_site_env(
#   api_token=os.getenv('FORGE_TOKEN'),
#   server_id=os.getenv('FORGE_SERVER_ID'),
#   site_name='ci-pr-environments.api.app.bizhaven.com',
#   overrides=FORGE_ENV_OVERRIDES
# )
