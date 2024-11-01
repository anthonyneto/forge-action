import requests
from manage_functions import *

def forge_list_site_ssl(api_token, server_id, site_name):
  site_id = get_site_id(api_token, server_id, site_name)
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/certificates'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    if 'certificates' in response_json and isinstance(response_json['certificates'], list):
      for cert in response_json['certificates']:
        if cert.get('status') == 'installed':
          print("SSL Certificate: Ready")
          return "installed"
        else:
          print("SSL Certificate: Installing")
          return "install"
    else:
        print("Unexpected response structure from forge_list_site_ssl:", response_json)
        return None

  except requests.RequestException as e:
    handle_request_error(e, "SSL: ")
    return None  

def forge_install_site_ssl(api_token, server_id, site_name):
  print('Checking SSL:')
  site_id = get_site_id(api_token, server_id, site_name)
  url = f'https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/certificates/letsencrypt'
  headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
  }
  payload = {
    'domains': [site_name,f"www.{site_name}"]
  }

  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    if 'certificate' in response_json:
      print("SSL Certificate: Ready")
      return response_json
    else:
      print("Unexpected response structure from forge_manage_site_ssl:", response_json)
      return None

  except requests.RequestException as e:
    handle_request_error(e, "SSL: ")
    return None  

def forge_manage_site_ssl(api_token, server_id, site_name):
  status = forge_list_site_ssl(api_token, server_id, site_name)

  if 'installed' != status:
    forge_install_site_ssl(api_token, server_id, site_name)
