import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone

from article.tasks import process_news_articles_by_time_period


def _parse_date(date_str, is_start=True):
    try:
        # Attempt to parse full date-time string (ISO format)
        return timezone.make_aware(
            datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S'),
            timezone.get_current_timezone()
        )
    except ValueError:
        try:
            # Attempt to parse only date (YYYY-MM-DD), append time
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            if is_start:
                # If it's the start date, set time to 00:00:00
                return timezone.make_aware(
                    date.replace(hour=0, minute=0, second=0),
                    timezone.get_current_timezone()
                )
            else:
                # If it's the end date, set time to 23:59:59
                return timezone.make_aware(
                    date.replace(hour=23, minute=59, second=59),
                    timezone.get_current_timezone()
                )
        except ValueError:
            raise CommandError('Dates must be in the format YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD')


class Command(BaseCommand):
    help = 'Runs an article-related task between a date range with optional time.'

    def add_arguments(self, parser):
        parser.add_argument(
            'date_from',
            type=str,
            help='Start date in the format YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD'
        )
        parser.add_argument(
            'date_to',
            type=str,
            help='End date in the format YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD'
        )
        parser.add_argument(
            '-c',
            '--country',
            nargs='+',
            default=settings.NEWS_COUNTRIES,
            help='List of country codes. Default is ["ca"].'
        )
        parser.add_argument(
            '-l',
            '--lang',
            nargs='+',
            default=settings.NEWS_LANGUAGES,
            help='List of language codes. Default is ["en"].'
        )
        parser.add_argument(
            '-s',
            '--split',
            nargs='+',
            default='hour',
            help='Time split. Values: hour, day, none. Default: hour'
        )

    def handle(self, *args, **options):
        date_from_str = options['date_from']
        date_to_str = options['date_to']
        countries = options['country']
        languages = options['lang']
        split = options['split']

        # Convert date strings to datetime objects with fallback to full-day if no time is provided
        date_from = _parse_date(date_from_str, is_start=True)
        date_to = _parse_date(date_to_str, is_start=False)

        if date_from > date_to:
            raise CommandError('--date-from cannot be later than --date-to')

        print("Started fetching and rewrite process...")
        count = process_news_articles_by_time_period(
            date_from, date_to, countries=countries, languages=languages, split='split'
        )

        print(self.style.SUCCESS(
            f'Successfully processed articles from {date_from} to {date_to}. Total count: {count}')
        )
