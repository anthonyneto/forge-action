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

    content = response.text

    if not content:
      print("The response content is empty.")
    else:
      print(content)

  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
  except Exception as err:
    print(f"An error occurred: {err}")

# Example usage
get_environment_variables(683662, 2477874)
