import endpoints as ep

async def retrieve_project_members(project_id, app_token, auth_token):
    """
    Retrieve the members of a project.

    Args:
        project_id (str): The ID of the project.
        app_token (str): The application token.
        auth_token (str): The authentication token.

    Returns:
        dict: The dictionary containing the user ID and name of each project member, or None if the retrieval fails.
    """
    endpoint = f"/v236/tasks/{project_id}/members"
    url = ep.base_url + endpoint

    page_start_id = 0
    page_limit = 5

    include_removed = 1
    include = ["users"]

    try:
        async with ep.aiohttp.ClientSession() as session:
            headers = {
                "AppToken": app_token,
                "AuthToken": auth_token,
                "pageLimit": str(page_limit),
            }

            params = {
                "page_start_id": page_start_id,
                "include_removed": include_removed,
                "include": include,
            }

            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    members = data["members"]
                    users = data["users"]

                    user_dict = {}

                    for member in members:
                        user_id = member["user_id"]
                        for user in users:
                            if user["id"] == user_id:
                                name = user["name"]
                                user_dict["user_id"] = user_id
                                user_dict["name"] = name
                                break

                    return user_dict
                else:
                    error_message = await response.text()
                    print(
                        f"Failed to retrieve project members with status code {response.status}: {error_message}"
                    )
    except ep.aiohttp.ClientError as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None