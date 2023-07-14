import logging
import endpoints as ep
from utilities.current_time import get_current_date
from utilities.api_exceptions import APIError

# Create a logger instance
logger = logging.getLogger(__name__)

async def retrieve_daily_activities_time(app_token, auth_token, organ_id):
    """
    Retrieve the daily activities time for users on different projects.

    Args:
        app_token (str): The application token.
        auth_token (str): The authentication token.
        organ_id (str): The ID of the organization.

    Returns:
        dict: A dictionary containing project IDs as keys and their corresponding project information as values.
              Each project information includes the project name and a list of dictionaries containing user IDs
              and their tracked time.
    """
    endpoint = f"/v236/organization/{organ_id}/activity/daily"
    url = ep.base_url + endpoint

    page_start_id = 0
    page_limit = 5

    current_date = get_current_date()

    headers = {
        "AppToken": app_token,
        "AuthToken": auth_token,
        "PageLimit": str(page_limit),
        #"DateStart": current_date,
        #"DateStop": current_date
        "DateStart" : "2023-07-12",
        "DateStop" : "2023-07-12"
    }

    params = {"page_start_id": page_start_id, "include": ["users", "projects"]}

    try:
        async with ep.aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    projects = data.get("projects", [])
                    daily_activities = data.get("daily_activities", [])
                    
                    project_info = {}

                    for project in projects:
                        project_id = project.get("id")
                        project_name = project.get("name")
                        project_info[project_id] = {
                            "project_name": project_name,
                            "user_ids": {}
                        }

                    for activity in daily_activities:
                        project_id = activity.get("project_id")
                        user_id = activity.get("user_id")
                        tracked_time = activity.get("tracked")
                        if project_id in project_info:
                            if user_id in project_info[project_id]["user_ids"]:
                                project_info[project_id]["user_ids"][user_id] += tracked_time
                            else:
                                project_info[project_id]["user_ids"][user_id] = tracked_time

                    # Convert tracked time dictionary to list of dictionaries
                    for project_id, info in project_info.items():
                        user_info_list = [
                            {"user_id": user_id, "tracked_time": tracked_time}
                            for user_id, tracked_time in info["user_ids"].items()
                        ]
                        info["user_ids"] = user_info_list

                    return project_info
                
                else:
                    error_message = await response.text()
                    logger.error(
                        f"Failed to retrieve daily activities with status code {response.status}: {error_message}"
                    )
                    raise APIError(f"Failed to retrieve daily activities with status code {response.status}")

    except Exception as e:
        logger.error(f"Error occurred during API call: {e}")
        raise APIError("Error occurred during API call")
