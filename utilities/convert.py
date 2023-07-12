from datetime import timedelta

"""
it took me a bit of time to noticed tracked time was actually in seconds 

did a lot of trial and errors

tried inspect the html too 
"""
async def convert_secs_hour(tracked_time):

    tracked_timedelta = timedelta(seconds=tracked_time)
    tracked_time_formatted = str(tracked_timedelta)

    return tracked_time_formatted
