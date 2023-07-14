class DataFilteringError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


async def filter_data(daily_activities, employees_names):
    try:
        user_id = list(employees_names.keys())[0]
        username = employees_names[user_id]

        filtered_data = {'username': username, 'projects': []}

        for _, info in daily_activities.items():
            for user_info in info['user_ids']:
                if user_info['user_id'] == user_id:
                    filtered_data['projects'].append({'project_name': info['project_name'], 'tracked_time': user_info['tracked_time']})

        return filtered_data

    except Exception as e:
        raise DataFilteringError("Error occurred during data filtering.") from e
