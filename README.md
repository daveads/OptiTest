# OptiTest

OptiTest is a project for managing test organizations and tracking project activities for [hubstaff](https://developer.hubstaff.com/docs/hubstaff_v2#!/activities/getV2OrganizationsOrganizationIdActivitiesDaily)

## Requirements
- Python
- Redis

## Installation

1. Create a Python virtual environment:

```bash
python -m venv env
```

2. Activate the virtual environment:

```bash
# For Linux and macOS
source env/bin/activate

# For Windows (PowerShell)
.\env\Scripts\Activate.ps1

# For Windows (Command Prompt)
.\env\Scripts\activate.bat
```

3. Install the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

## Installing on a Server

1. Clone the OptiTest repository:

```bash
git clone git@github.com:daveads/OptiTest.git
```

2. Set executable permissions for the appropriate wrapper script:

```bash
# For Bash
chmod +x cron_wrap.sh

# For Python
chmod +x cron_wrap.py
```

## Configuration

1. Create a `.env` file in the project root directory with the following configuration:

```
APP_TOKEN="DYC85JIPGET1Kdfd"  # App token <string>
EMAIL="the.thte@gmail.com"  # Email <string>
PASSWORD="000"  # Password <string>
ORGANIZATION=000000  # Organization ID <integer>

output_dir="/path/to/output/directory"  # Output directory for the generated HTML <string>

directory="/path/to/script/directory"  # OptiTest directory <string>

Manager_email="manager@example.com"  # Manager's email <string>
```

## Usage

1. Run the OptiTest project using the appropriate wrapper script:

```bash
# For Bash
./cron_wrap.sh

# For Python
./cron_wrap.py
```

## Cron Tab Setup

To schedule the OptiTest project to run automatically, set up a cron job using the following steps:

1. Open the crontab for editing:
```bash
crontab -e
```

2. Add the following line at the end to run the `/path/to/cron_wrapper.sh` script daily at 11:50 PM:
```bash
50 23 * * * /path/to/cron_wrapper.sh
```
Make sure to replace `/path/to/cron_wrapper.sh` with the actual path to the `cron_wrapper.sh` or `cron_wrapper.py` script.

3. Save and exit the crontab file.

> Note: Ensure that the cron job is set up correctly and the script file has the necessary permissions to execute.

## Redis Configuration

OptiTest uses the default Redis configuration.

Please make sure to replace `/path/to/output/directory` and `/path/to/script/directory` with the appropriate directory paths in the `.env` file.
```

Feel free to further customize the content and instructions to suit your project's specific requirements.