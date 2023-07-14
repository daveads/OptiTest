import logging
import endpoints as ep
from utilities.api_exceptions import APIError

# Create a logger instance
logger = logging.getLogger(__name__)

async def retrieve_organization_members(organization_id, app_token, auth_token):
    endpoint = f"/v236/organization/{organization_id}/members"
    url = ep.base_url + endpoint

    page_start_id = 0
    page_limit = 5
    include_removed = 1
    include_projects = 1
    include = ["users"]

    headers = {
        "AppToken": app_token,
        "AuthToken": auth_token,
        "PageLimit": str(page_limit),
        "IncludeProjects": str(include_projects)
    }

    params = {
        "page_start_id": page_start_id,
        "include_removed": include_removed,
        "include": include
    }

    try:
        async with ep.aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    json_data = await response.json()

                    users = json_data.get("users", [])
                    user_dict = {}

                    for user in users:
                        user_id = user.get("id")
                        name = user.get("name")
                        user_dict[user_id] = name

                    return user_dict
                
                else:
                    error_message = await response.text()

                    logger.error(
                        f"Failed to retrieve organization projects with status code {response.status} : {error_message}"
                    )
                    raise APIError(f"Failed to retrieve organization projects with status code {response.status}")

    except Exception as e:
        logger.error(f"Error occurred while retrieving organization projects: {e}")
        raise APIError("Error occurred while retrieving organization projects")
