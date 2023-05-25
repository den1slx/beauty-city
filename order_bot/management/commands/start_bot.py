from django.core.management.base import BaseCommand
from order_bot.bot_handlers import run_bot


class Command(BaseCommand):
    help = 'run bot'

    def handle(self, *args, **options):
        run_bot()
