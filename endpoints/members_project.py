import endpoints as ep


async def retrieve_project_members(project_id, app_token, auth_token):
    endpoint = f"/v236/tasks/{project_id}/members"
    url = ep.base_url + endpoint

    page_start_id = 0
    page_limit = 5

    include_removed = 1
    include = ["users"]

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
                return None
