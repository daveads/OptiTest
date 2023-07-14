from datetime import timedelta

async def convert_secs_hour(tracked_time):
    """
    Convert tracked time from seconds to hour format.

    Args:
        tracked_time (int): The tracked time in seconds.

    Returns:
        str: The tracked time formatted as hours.
    """
    tracked_timedelta = timedelta(seconds=tracked_time) 
    tracked_time_formatted = str(tracked_timedelta)

    return tracked_time_formatted