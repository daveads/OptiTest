#!/usr/bin/env python

import asyncio
from dotenv import load_dotenv
import os

# Endpoints
from endpoints import signin
from endpoints import retrieve_org_project as orgproject
from endpoints.members_project import retrieve_project_members
from endpoints.daily_org_act import retrieve_daily_activities_time

#utilities
from utilities.convert import convert_secs_hour

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_TOKEN = os.getenv("APP_TOKEN")
PASSWORD = os.getenv("PASSWORD")
ORGANIZATION = os.getenv("ORGANIZATION")


async def main():
    auth_token = await signin.signin(APP_TOKEN, EMAIL, PASSWORD)
    
    projects = await orgproject.retieve_organization_projects(ORGANIZATION, APP_TOKEN, auth_token)
    
    member = await retrieve_project_members(2586858, APP_TOKEN, auth_token)

    tracked_time = await retrieve_daily_activities_time(2302746,2586858, APP_TOKEN, auth_token)
    
    print(member)
    print(projects)

    print(await convert_secs_hour(tracked_time))
    

if __name__ == "__main__":
    asyncio.run(main())
