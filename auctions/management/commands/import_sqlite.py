import os
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from auctions.models import Auction, Bid, Category, Comment, NotificationMsg, User, Watchlist


def parse_dt(value):
    # SQLite stores USE_TZ datetimes as naive UTC strings.
    if value is None:
        return None
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


class Command(BaseCommand):
    help = "Copy the auctions data from the old SQLite database into the current (MongoDB) database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=os.path.join(settings.BASE_DIR, "db.sqlite3"),
            help="Path to the SQLite file (default: db.sqlite3 in the project root).",
        )

    def handle(self, *args, **options):
        if not os.path.exists(options["path"]):
            raise CommandError(f"SQLite file not found: {options['path']}")
        if Category.objects.exists() or Auction.objects.exists():
            raise CommandError("Target database already has categories/auctions; refusing to import twice.")

        db = sqlite3.connect(options["path"])
        db.row_factory = sqlite3.Row
        rows = lambda table: db.execute(f"SELECT * FROM {table} ORDER BY id").fetchall()

        # Old integer id -> new object, per table.
        users, categories, auctions = {}, {}, {}

        for r in rows("auctions_user"):
            existing = User.objects.filter(username=r["username"]).first()
            if existing:
                # Keep accounts already created in MongoDB (e.g. via createsuperuser) as they are.
                users[r["id"]] = existing
                self.stdout.write(f"  user {r['username']}: already exists, reusing")
                continue
            users[r["id"]] = User.objects.create(
                username=r["username"],
                password=r["password"],  # already hashed
                email=r["email"],
                first_name=r["first_name"],
                last_name=r["last_name"],
                is_superuser=bool(r["is_superuser"]),
                is_staff=bool(r["is_staff"]),
                is_active=bool(r["is_active"]),
                last_login=parse_dt(r["last_login"]),
                date_joined=parse_dt(r["date_joined"]),
            )

        for r in rows("auctions_category"):
            categories[r["id"]] = Category.objects.create(name=r["name"])

        for r in rows("auctions_auction"):
            auction = Auction.objects.create(
                title=r["title"],
                description=r["description"],
                category=categories[r["category_id"]],
                price=Decimal(str(r["price"])),
                seller=users[r["seller_id"]],
                image=r["image"],
                active=bool(r["active"]),
                modify_date=parse_dt(r["modify_date"]),
            )
            # auto_now_add overwrites create_date on save, so restore it afterwards.
            Auction.objects.filter(pk=auction.pk).update(create_date=parse_dt(r["create_date"]))
            auctions[r["id"]] = auction

        for r in rows("auctions_bid"):
            bid = Bid.objects.create(
                auction=auctions[r["auction_id"]],
                user=users[r["user_id"]],
                amount=Decimal(str(r["amount"])),
            )
            Bid.objects.filter(pk=bid.pk).update(date=parse_dt(r["date"]))

        for r in rows("auctions_comment"):
            comment = Comment.objects.create(
                auction_item=auctions[r["auction_item_id"]],
                user=users[r["user_id"]],
                comment=r["comment"],
            )
            Comment.objects.filter(pk=comment.pk).update(date=parse_dt(r["date"]))

        for r in rows("auctions_watchlist"):
            Watchlist.objects.create(
                auction_item=auctions[r["auction_item_id"]],
                user=users[r["user_id"]],
            )

        for r in rows("auctions_notificationmsg"):
            notification = NotificationMsg.objects.create(
                user=users[r["user_id"]],
                auction_item=auctions[r["auction_item_id"]],
                message=r["message"],
                read=bool(r["read"]),
                is_status=bool(r["is_status"]),
            )
            NotificationMsg.objects.filter(pk=notification.pk).update(create_date=parse_dt(r["create_date"]))

        db.close()
        for model in (User, Category, Auction, Bid, Comment, Watchlist, NotificationMsg):
            self.stdout.write(f"{model.__name__}: {model.objects.count()}")
        self.stdout.write(self.style.SUCCESS("Import finished."))
