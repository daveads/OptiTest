import datetime


def get_current_date():
    """
    Get the current date.

    Returns:
        str: The current date in the format 'YYYY-MM-DD'.
    """
    current_date = datetime.datetime.now()  # Get the current date and time
    current_date_str = current_date.strftime("%Y-%m-%d")  # Format the date as 'YYYY-MM-DD'
    return current_date_str
