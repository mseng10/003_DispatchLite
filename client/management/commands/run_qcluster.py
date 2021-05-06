from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads example pipeline data into the database"

    def handle(self, *args, **options):
        send_mail(subject="PGSCM rate limit exceeded",
                  message='IT WOOOOOOOOORKS!!!!!!!!!!11',
                  from_email=settings.EMAIL_HOST_USER, recipient_list=['dnkelly97@gmail.com'],
                  fail_silently=False, auth_user=None,
                  auth_password=None, connection=None, html_message=None)
