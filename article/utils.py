from datetime import timedelta
from django.utils import timezone
from django.conf import settings


def split_into_days(date_from, date_to):
    day_list = []
    
    current_start = date_from
    while current_start < date_to:
        current_end = min(current_start + timedelta(days=1), date_to)
        day_list.append((current_start, current_end))
        current_start = current_end
    
    return day_list


from datetime import timedelta

def split_into_hours(date_from, date_to):
    hour_list = []
    
    current_start = date_from
    while current_start < date_to:
        current_end = min(current_start + timedelta(hours=1), date_to)
        
        # Skip the interval if it's less than 2 minutes
        if (current_end - current_start) < timedelta(minutes=2):
            break

        hour_list.append((current_start, current_end))
        current_start = current_end
    
    return hour_list
