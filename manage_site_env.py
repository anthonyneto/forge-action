import json
import requests
import os

def get_environment_variables(server_id, site_id):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN', 'your_forge_token')
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

def get_default_environment_variables(server_id, default_site_id):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN', 'your_forge_token')
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{default_site_id}/env"

  headers = {
    "Authorization": f"Bearer {FORGE_TOKEN}"
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred while fetching default environment variables: {err}")
  except Exception as err:
    print(f"An error occurred while fetching default environment variables: {err}")

def update_environment_variables(server_id, site_id, content):
  FORGE_TOKEN = os.getenv('FORGE_TOKEN', 'your_forge_token')
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/env"

  headers = {
    "Authorization": f"Bearer {FORGE_TOKEN}",
    "Content-Type": "application/json"
  }

  content_dict = {}
  for line in content.strip().split('\n'):
    line = line.strip()
    if line.startswith("#"):
      continue
    if '=' in line:
        key, value = line.split('=', 1)
        content_dict[key] = value.strip('"')
  content_json = json.dumps(content_dict, indent=2)
  payload = {
    "content": "world"
  }

  payload = json.dumps(payload, indent=4)
  print(payload)


  try:
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.text
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred while updating environment variables: {err}")
  except Exception as err:
    print(f"An error occurred while updating environment variables: {err}")

def main():
  server_id = 683662
  site_id = 2477874
  current_environment_variables = get_environment_variables(server_id, site_id)

  if not current_environment_variables:
    print("The response content is empty. Attempting to update environment variables.")
    updated_environment_variables = get_default_environment_variables(server_id, default_site_id=2097190)
    print(f"Updating Environment Variables")

    update_environment_variables(server_id, site_id, updated_environment_variables)
  else:
    print(current_environment_variables)

if __name__ == "__main__":
  main()
