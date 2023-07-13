import endpoints as ep  # package


async def retieve_organization_projects(organization_id, app_token, auth_token):
    endpoint = f"/v236/organization/{organization_id}/tasks"
    url = ep.base_url + endpoint

    status = "active"
    page_start_id = 0
    page_limit = 5
    include = ["clients"]

    headers = {
        "AppToken": app_token,
        "AuthToken": auth_token,
        "PageLimit": str(page_limit),
    }

    params = {"page_start_id": page_start_id, "status": status, "include": include}

    async with ep.aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                json_data = await response.json()

                projects = [
                    {"id": project["id"], "name": project["name"]}
                    for project in json_data["projects"]
                ]

                return projects

            else:
                error_message = await response.text()

                print(
                    f"Failed to retrieve organization projects with status code {response.status} : {error_message}"
                )
                return []
