from django.db.models import Q

from article.models import NewsChannelFetchLog


def get_unfetched_time_ranges(date_from, date_to, channel_name, source_id):
    # Fetch all successful logs for the given source and within the date range
    successful_logs = NewsChannelFetchLog.objects.filter(
        Q(channel_name=channel_name) &
        Q(source_id=source_id) & 
        Q(success=True) & 
        (
            (Q(date_from__gte=date_from) & Q(date_from__lt=date_to)) |  # Logs starting in the range
            (Q(date_to__gt=date_from) & Q(date_to__lte=date_to)) |      # Logs ending in the range
            (Q(date_from__lte=date_from) & Q(date_to__gte=date_to))     # Logs covering the whole range
        )
    ).order_by('date_from')

    # Initialize the list to store gaps
    unfetched_ranges = []

    # If no logs were successful, return the full original range as one gap
    if not successful_logs.exists():
        return [(date_from, date_to)]

    # Track the current gap start in the range
    current_start = date_from

    for log in successful_logs:
        # If there's a gap before the current successful log
        if log.date_from > current_start:
            # Add the gap (unfetched range) to the list
            unfetched_ranges.append((current_start, log.date_from))
        # Move the current start to the end of the successful log
        current_start = max(current_start, log.date_to)

    # If there's still a gap after the last successful log, add that gap
    if current_start < date_to:
        unfetched_ranges.append((current_start, date_to))

    # Return the list of unfetched time ranges
    return unfetched_ranges
