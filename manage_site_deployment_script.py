import requests
import textwrap
from manage_functions import *

def update_deployment_script(api_token, server_id, site_id, sitename):
  url = f"https://forge.laravel.com/api/v1/servers/{server_id}/sites/{site_id}/deployment/script"
  headers = {'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}

  deployment_script = textwrap.dedent(f'''\
    cd /home/forge/{sitename}
    git pull origin $FORGE_SITE_BRANCH

    $FORGE_COMPOSER install --no-dev --no-interaction --prefer-dist --optimize-autoloader

    ( flock -w 10 9 || exit 1
        echo 'Restarting FPM...'; sudo -S service $FORGE_PHP_FPM reload ) 9>/tmp/fpmlock

    if [ -f artisan ]; then
      $FORGE_PHP artisan cache:clear
      $FORGE_PHP artisan view:clear
      $FORGE_PHP artisan config:clear
      $FORGE_PHP artisan event:clear

      $FORGE_PHP artisan view:cache
      $FORGE_PHP artisan config:cache
      $FORGE_PHP artisan event:cache

      $FORGE_PHP artisan storage:link

      $FORGE_PHP artisan migrate --force

      $FORGE_PHP artisan queue:restart
    fi
  ''')

  payload = {
    "content": deployment_script
  }

  try:
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.text
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred while updating environment variables: {err}")
  except Exception as err:
    print(f"An error occurred while updating environment variables: {err}")

def forge_manage_site_deployment_script(api_token, server_id, site_name):
  print('Starting Update: Deployment Script')
  site_id = get_site_id(api_token, server_id, site_name)
  update_deployment_script(api_token, server_id, site_id, site_name)
  print('Finished Update: Deployment Script')
