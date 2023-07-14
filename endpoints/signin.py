import logging
import endpoints as ep
from utilities.api_exceptions import APIError

# Create a logger instance
logger = logging.getLogger(__name__)

async def signin(app_token, email, password):
    """
    Function to perform the sign-in process.

    Args:
        app_token (str): The application token.
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str: The authentication token if sign-in is successful, None otherwise.
    """
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
                    logger.error(f"Sign-in failed with status code {response.status}")
                    raise APIError(f"Sign-in failed with status code {response.status}")

    except Exception as e:
        logger.error(f"Error occurred during sign-in: {e}")
        raise APIError("Error occurred during sign-in")
