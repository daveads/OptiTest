import asyncio
from dotenv import load_dotenv
import os
import sys
import time

# Endpoints
from endpoints.signin import signin
from endpoints.retrieve_org_project import retrieve_organization_projects
from endpoints.members_project import retrieve_project_members
from endpoints.daily_org_act import retrieve_daily_activities_time

# utils
from utilities.convert import convert_secs_hour
from utilities.current_time import get_current_date
from utilities.redis_cache import setkey

load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_TOKEN = os.getenv("APP_TOKEN")
PASSWORD = os.getenv("PASSWORD")
ORGANIZATION = os.getenv("ORGANIZATION")


async def main():
    start_time = time.time()

    # Retrieve the authentication token
    auth_token = asyncio.ensure_future(signin(APP_TOKEN, EMAIL, PASSWORD))
    auth_tok = await auth_token

    # Retrieve the organization projects
    projects_task = asyncio.ensure_future(retrieve_organization_projects(ORGANIZATION, APP_TOKEN, auth_tok))
    await asyncio.gather(auth_token, projects_task)

    cached_auth = setkey("auth_token", auth_token)

    if cached_auth:
        auth_tok = cached_auth
        # print("cached_auth")
    else:
        auth_tok = await auth_token
        # print("auth_token")

    projects = await projects_task

    tasks = []

    for project in projects:
        members_task = await retrieve_project_members(project["id"], APP_TOKEN, auth_tok)
        timespent_task = await retrieve_daily_activities_time(
            members_task["user_id"], project["id"], APP_TOKEN, auth_tok, ORGANIZATION
        )
        tasks.append((project, members_task, timespent_task))

    data = {
        project["name"]
        .lower()
        .replace(" ", ""): {
            "id": project["id"],
            member_response["name"]: {
                "userid": member_response["user_id"],
                "time": await convert_secs_hour(timespent_response),
            },
        }
        for project, member_response, timespent_response in tasks
    }

    result = [
        (member_name, project_name, member_data["time"])
        for project_name, project_data in data.items()
        for member_name, member_data in project_data.items()
        if member_name != "id"
    ]

    # Group employee names
    employee_names = list(set(name for name, _, _ in result))
    employee_names.sort()

    html_table = """
    <table>
        <thead>
            <tr>
                <th>Employee</th>
                <th>Project</th>
                <th>Time Spent</th>
            </tr>
        </thead>
        <tbody>
    """

    for name in employee_names:
        projects = [proj for emp, proj, _ in result if emp == name]
        time_spent = [time for emp, _, time in result if emp == name]
        num_projects = len(projects)

        if num_projects > 0:
            html_table += f"""
            <tr>
                <td rowspan='{num_projects}'>{name}</td>
                <td>{projects[0]}</td>
                <td>{time_spent[0]}</td>
            </tr>
            """

            for i in range(1, num_projects):
                html_table += f"""
                <tr>
                    <td>{projects[i]}</td>
                    <td>{time_spent[i]}</td>
                </tr>
                """

    html_table += """
        </tbody>
    </table>
    """

    sys.stdout.write(html_table)

    end_time = time.time()
    execution_time = end_time - start_time
    #print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
