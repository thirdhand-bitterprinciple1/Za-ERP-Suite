import secrets

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Rotate passwords and tokens for demo users used in local testing."

    demo_usernames = [
        "admin",
        "manager",
        "sales",
        "inventory",
        "accounting",
        "purchasing",
        "hr",
        "projects",
        "finance_globex",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Optional shared password for all demo users. If omitted, each user gets a random password.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        shared_password = options.get("password")

        self.stdout.write(self.style.SUCCESS("Rotated demo credentials:"))
        self.stdout.write("username | password | token")

        for username in self.demo_usernames:
            user = user_model.objects.filter(username=username).first()
            if not user:
                self.stdout.write(f"{username} | not found | not found")
                continue

            password = shared_password or secrets.token_urlsafe(14)
            user.set_password(password)
            user.save(update_fields=["password"])

            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            self.stdout.write(f"{username} | {password} | {token.key}")

        self.stdout.write("")
        self.stdout.write("Required request headers:")
        self.stdout.write("Authorization: Token <token>")
        self.stdout.write("X-Company-ID: <company_id>")
