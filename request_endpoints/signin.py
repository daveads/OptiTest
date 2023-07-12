import request_endpoints as reqs #package 



async def signin(app_token, email, password):

    endpoint = "/v236/people/signin"
    url = reqs.base_url + endpoint

    headers = {
    "AppToken": app_token
    }

    payload = {
        "email": email,
        "password": password
    }

    
    async with reqs.aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            if response.status == 200:
                
                data = await response.json()
                auth_token = data["auth_token"]
                return auth_token
            
            else: 
                print(f"sign-in failed with status code {response.status}") # use logger 
                return None 