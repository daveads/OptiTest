#!/usr/bin/env python
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from utilities.current_time import get_current_date
from utilities.email_sender import send_email

async def main():
    load_dotenv(".env")

    directory = os.getenv("directory")

    # Email setup
    sever_company_email = os.getenv('sever_company_email')
    sever_company_password = os.getenv('sever_company_password')
    manager_email = [f"{os.getenv('Manager_email')}"]

    os.chdir(directory)

    process = await asyncio.create_subprocess_shell(
        "python3 main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    output, _ = await process.communicate()
    output = output.decode()

    await send_email(output, sever_company_email, sever_company_password, manager_email)

    output_dir = os.getenv("output_dir")

    current_date = get_current_date()
    output_file = os.path.join(output_dir, f"output_{current_date}.html")

    with open(output_file, "w") as file:
        file.write(output)

    os.chmod(output_file, 0o644)

if __name__ == "__main__":
    asyncio.run(main())
