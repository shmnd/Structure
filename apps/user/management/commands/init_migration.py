from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    help = "combaining 2 migrations commands into 1 command 'init-migration' "

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
