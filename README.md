# Forge Action

This GitHub Action allows you to create and manage environments via the Laravel Forge API. It simplifies the process of setting up and deploying your applications by automating the necessary API calls to Forge.

## Inputs

This action requires the following inputs:

- **GITHUB_BRANCH_NAME**: The name of the Git branch to be used for deployment. (Required)

- **RDS_ROOT_USERNAME**: The root username for the RDS database. (Required)

- **RDS_ROOT_PASSWORD**: The root password for the RDS database. (Required)

- **RDS_NAME**: The name of the RDS database to be created or used. (Required)

- **RDS_PR_DB_NAME**: The name of the RDS database for your application. (Required)

- **FORGE_API_TOKEN**: API token used for authenticating Forge API requests. (Required)

- **FORGE_SERVER_ID**: The ID of the server managed by Forge where the site will be created. (Required)

- **FORGE_ZONE**: The DNS zone to be used by the Forge site for domain configuration. (Required)

- **FORGE_GIT_URL**: The URL of the Git repository to be used by Forge for deployment. (Required)

## Usage

To use this action in your GitHub workflow, you need to define it in your workflow YAML file. Here is an example of how to use the Forge Action:

```yaml
name: Deploy to Forge

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Get Branch Name
        run: |
          GITHUB_BRANCH_NAME="${GITHUB_REF#refs/heads/}"
          echo "GITHUB_BRANCH_NAME=$GITHUB_BRANCH_NAME" >> $GITHUB_ENV

      - name: Deploy to Forge
        uses: your-username/forge-action@v1
        with:
          GITHUB_BRANCH_NAME: ${{ env.GITHUB_BRANCH }}
          RDS_ROOT_USERNAME: ${{ secrets.RDS_ROOT_USERNAME }}
          RDS_ROOT_PASSWORD: ${{ secrets.RDS_ROOT_PASSWORD }}
          RDS_NAME: 'mydatabase'
          RDS_PR_DB_NAME: 'myappdb'
          FORGE_API_TOKEN: ${{ secrets.FORGE_API_TOKEN }}
          FORGE_SERVER_ID: '123456'
          FORGE_ZONE: 'example.com'
          FORGE_GIT_URL: 'username/project'
