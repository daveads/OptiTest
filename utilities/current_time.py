import datetime


def get_current_date():
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%Y-%m-%d")
    return current_date_str
