#!/usr/bin/env python

import os
from datetime import datetime
from dotenv import load_dotenv
from utilities.current_time import get_current_date

load_dotenv(".env")

directory = os.getenv("directory")

os.chdir(directory)

output = os.popen("python3 main.py").read()

output_dir = os.getenv("output_dir")


current_date = get_current_date()
output_file = os.path.join(output_dir, f"output_{current_date}.html")

with open(output_file, "w") as file:
    file.write(output)


os.chmod(output_file, 0o644)
