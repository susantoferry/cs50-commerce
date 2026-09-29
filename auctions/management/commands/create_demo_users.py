from django.core.management.base import BaseCommand

from auctions.models import User

DEMO_USERNAMES = ["ferry", "keele", "stacy", "chris"]
DEMO_PASSWORD = "password"


class Command(BaseCommand):
    help = "Create the demo accounts shown on the login page (or reset their passwords)."

    def handle(self, *args, **options):
        # The old SQLite data calls keele "ichi"; rename it so its bids and comments carry over.
        if not User.objects.filter(username="keele").exists():
            User.objects.filter(username="ichi").update(username="keele", email="keele@test.com")

        for username in DEMO_USERNAMES:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": f"{username}@test.com"}
            )
            user.set_password(DEMO_PASSWORD)
            user.save()
            self.stdout.write(f"{username}: {'created' if created else 'password reset'}")
