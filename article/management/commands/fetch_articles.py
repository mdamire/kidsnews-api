import datetime
from django.core.management.base import BaseCommand, CommandError
from article.tasks import featch_and_rewrite_news_articles

class Command(BaseCommand):
    help = 'Runs an article-related task between a date range.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date-from',
            type=str,
            help='Start date in the format YYYY-MM-DD',
            required=True
        )
        parser.add_argument(
            '--date-to',
            type=str,
            help='End date in the format YYYY-MM-DD',
            required=True
        )

    def handle(self, *args, **options):
        date_from_str = options['date_from']
        date_to_str = options['date_to']

        # Convert date strings to date objects
        try:
            date_from = datetime.datetime.strptime(date_from_str, '%Y-%m-%d').date()
            date_to = datetime.datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            raise CommandError('Dates must be in the format YYYY-MM-DD')

        if date_from > date_to:
            raise CommandError('--date-from cannot be later than --date-to')

        print("Started featching and rewrite process...")
        count = featch_and_rewrite_news_articles(date_from, date_to)

        print(self.style.SUCCESS(
            f'Successfully processed articles from {date_from} to {date_to}. Total count: {count}')
        )
