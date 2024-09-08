import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone

from article.tasks import process_news_articles_by_time_period

class Command(BaseCommand):
    help = 'Runs an article-related task between a date range.'

    def add_arguments(self, parser):
        parser.add_argument(
            'date_from',
            type=str,
            help='Start date in the format YYYY-MM-DD'
        )
        parser.add_argument(
            'date_to',
            type=str,
            help='End date in the format YYYY-MM-DD'
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

    def handle(self, *args, **options):
        date_from_str = options['date_from']
        date_to_str = options['date_to']
        countries = options['country']
        languages = options['lang']

        # Convert date strings to date objects
        try:
            date_from = timezone.make_aware(
                datetime.datetime.strptime(date_from_str, '%Y-%m-%d'),
                timezone.get_current_timezone()
            )
            date_to = timezone.make_aware(
                datetime.datetime.strptime(date_to_str, '%Y-%m-%d'),
                timezone.get_current_timezone()
            )
            # Set date_to to the end of the day
            date_to = date_to.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            raise CommandError('Dates must be in the format YYYY-MM-DD')

        if date_from > date_to:
            raise CommandError('--date-from cannot be later than --date-to')

        print("Started fetching and rewrite process...")
        count = process_news_articles_by_time_period(
            date_from, date_to, countries=countries, languages=languages
        )

        print(self.style.SUCCESS(
            f'Successfully processed articles from {date_from} to {date_to}. Total count: {count}')
        )
