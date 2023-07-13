import endpoints as ep  # package


async def signin(app_token, email, password):
    endpoint = "/v236/people/signin"
    url = ep.base_url + endpoint

    headers = {"AppToken": app_token}

    payload = {"email": email, "password": password}

    try:
        async with ep.aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    auth_token = data.get("auth_token")
                    return auth_token
                else:
                    print(f"Sign-in failed with status code {response.status}")  # Use a logger for better error handling
                    return None
    except ep.aiohttp.ClientError as e:
        print(f"Error occurred during sign-in: {e}")
        return None
