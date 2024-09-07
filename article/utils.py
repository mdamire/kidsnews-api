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
    
    yield day_list
