import endpoints as ep

async def retrieve_daily_activities_time(user_id, project_id, app_token, auth_token):

    #organization_id = ep.organization_id

    endpoint = f"/v236/organization/{ep.organization_id}/activity/daily"
    url = ep.base_url + endpoint

    page_start_id = 0
    page_limit = 5


    headers = {
        "AppToken" : app_token,
        "AuthToken" : auth_token,
        "PageLimit" : str(page_limit),
        "DateStart" : "2023-07-12",
        "DateStop" : "2023-07-16",
        "UserIds" : str(user_id),
        "ProjectIds" : str(project_id)
    }


    params = {
        "page_start_id" : page_start_id,
        "include" : ["users", "tasks", "projects"]
    }


    async with ep.aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()

                daily_activities = data.get('daily_activities', [])
                tracked_time = 0
                if daily_activities:
                    tracked_time = daily_activities[0].get('tracked', 0)
                return tracked_time
            

            else:
                error_message = await response.text()
                print(f"Failed to retrieve daily activities with status code {response.status} : {error_message}")
                return None