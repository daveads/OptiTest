import asyncio
from dotenv import load_dotenv
import logging
import os
import sys
import time

# Endpoints
from endpoints.signin import signin
from endpoints.retrive_org_members import retrieve_organization_members
from endpoints.members_project import retrieve_project_members
from endpoints.daily_org_act import retrieve_daily_activities_time, APIError




# Utils
from utilities.convert import convert_secs_hour
from utilities.current_time import get_current_date
from utilities.redis_cache import setkey, CacheError
from utilities.data_filter import filter_data
from utilities.html import generate_html_table

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_TOKEN = os.getenv("APP_TOKEN")
PASSWORD = os.getenv("PASSWORD")
ORGANIZATION = os.getenv("ORGANIZATION")

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    start_time = time.time()

    try:
        # Retrieve the authentication token
        auth_token = await signin(APP_TOKEN, EMAIL, PASSWORD)

        cached_auth = setkey("auth_token", auth_token)

        if cached_auth:
            auth_tok = cached_auth
        else:
            auth_tok = await auth_token


        daily_activities = asyncio.ensure_future(retrieve_daily_activities_time(APP_TOKEN, auth_tok,ORGANIZATION,))

        
        # Retrieve the organization members
        
        employees_names = asyncio.ensure_future(retrieve_organization_members(ORGANIZATION, APP_TOKEN, auth_tok))

        await asyncio.gather(daily_activities, employees_names)


        employees = await employees_names
        activities = await daily_activities 

        # Convert tracked time to hours
        for _, project_data in activities.items():
            user_ids = project_data['user_ids']
            for user in user_ids:
                tracked_time_seconds = user['tracked_time']
                tracked_time_hours = await convert_secs_hour(tracked_time_seconds)
                user['tracked_time'] = tracked_time_hours



        #filtered data
        Data = await filter_data(activities, employees)

        html_table = await generate_html_table(Data)
        sys.stdout.write(html_table)

    except CacheError as e:
        logger.error(f"Cache error occurred: {e}")
        # Handle the CacheError and log the error message

    except APIError as e:
        logger.error(f"API error occurred: {e}")

    except Exception as e:
        logger.exception("An unexpected error occurred")
        # Log the exception stack trace and handle the unexpected error

    end_time = time.time()
    execution_time = end_time - start_time
    #print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
