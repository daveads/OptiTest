#!/usr/bin/env python

import asyncio
from dotenv import load_dotenv
import os

from endpoints import signin
from endpoints import retrieve_org_project as orgproject

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_TOKEN = os.getenv("APP_TOKEN")
PASSWORD = os.getenv("PASSWORD")
ORGANIZATION = os.getenv("ORGANIZATION")


async def main():
    auth_token = await signin.signin(APP_TOKEN, EMAIL, PASSWORD)
    
    projects = await orgproject.retieve_organization_projects(ORGANIZATION, APP_TOKEN, auth_token)

    # get members in a project

    #[{'id': 2586857, 'name': 'Project A'}, {'id': 2586858, 'name': 'hubstaff bot467'}, {'id': 2586859, 'name': 'Project B'}]


    
    #print(auth_token)


if __name__ == "__main__":
    asyncio.run(main())
