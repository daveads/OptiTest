#!/usr/bin/env python

import asyncio
from dotenv import load_dotenv
import os

from request_endpoints import signin

EMAIL = os.getenv("EMAIL")
APP_TOKEN = os.getenv("APP_TOKEN")
PASSWORD = os.getenv("PASSWORD")


load_dotenv()


async def main():
    auth_token = await signin.signin(APP_TOKEN, EMAIL, PASSWORD)

    print(auth_token)


if __name__ == "__main__":
    asyncio.run(main())
