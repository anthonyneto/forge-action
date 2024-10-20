import requests
from manage_functions import *

def get_environment_variables(api_token, server_id, site_id):
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/env"
  headers = {'Authorization': f'Bearer {api_token}'}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
  except Exception as err:
    print(f"An error occurred: {err}")

def update_environment_variables(api_token, server_id, site_id, content, overrides):
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/env"
  headers = {'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}

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
  print('Starting Update: .env')
  site_id = get_site_id(api_token, server_id, site_name)
  current_environment_variables = get_environment_variables(api_token, server_id, site_id)

  max_attempts = 6
  attempts = 0

  while attempts < max_attempts:
    if not current_environment_variables:
      current_environment_variables = get_environment_variables(api_token, server_id, site_id)
      if current_environment_variables:
        print(f"Success")
        break
    else:
      # continue since .env was successfully returned
      break

    attempts += 1
    print(f"Attempt {attempts} failed. Retrying in 5 seconds...")
    time.sleep(5)

  if attempts == max_attempts:
    print("Failed to update variable after 5 attempts.")

  site_data = check_site_status(api_token, server_id, site_id)
  if not site_data:
    print("Failed to confirm site status after creation.")
    return
  update_environment_variables(api_token, server_id, site_id, current_environment_variables, overrides)
  print('Finished Update: .env')
