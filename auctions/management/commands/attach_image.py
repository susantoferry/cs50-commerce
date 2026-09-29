import mimetypes

from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse

from auctions.models import Auction, AuctionImage

mimetypes.add_type("image/webp", ".webp")


class Command(BaseCommand):
    help = "Store an image file in MongoDB and use it as the auction's picture."

    def add_arguments(self, parser):
        parser.add_argument("auction_id", help="ObjectId of the auction.")
        parser.add_argument("path", help="Path to the image file.")

    def handle(self, *args, **options):
        try:
            auction = Auction.objects.get(pk=options["auction_id"])
        except Auction.DoesNotExist:
            raise CommandError(f"No auction with id {options['auction_id']}")

        content_type, _ = mimetypes.guess_type(options["path"])
        if not content_type or not content_type.startswith("image/"):
            raise CommandError(f"Not a recognised image file: {options['path']}")

        with open(options["path"], "rb") as f:
            data = f.read()

        AuctionImage.objects.update_or_create(
            auction=auction, defaults={"data": data, "content_type": content_type}
        )
        auction.image = reverse("auction_image", args=(auction.id,))
        auction.save()
        self.stdout.write(self.style.SUCCESS(
            f"Stored {len(data)} bytes ({content_type}) for '{auction.title}' -> {auction.image}"
        ))
