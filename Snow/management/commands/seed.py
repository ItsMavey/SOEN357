"""
Management command to seed the database with demo users, postings, and ratings.

Usage:
    python manage.py seed          # seed once (skips if data exists)
    python manage.py seed --flush  # wipe and re-seed
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from Snow.models import EXIFMetadata, Posting, Rating, UserProfile, WorkProof

User = get_user_model()

# Paths to the generated demo images (committed to repo)
DEMO_IMG_DIR = Path(__file__).resolve().parent / "demo_images"

USERS = [
    {
        "username": "maya.chen",
        "first_name": "Maya",
        "last_name": "Chen",
        "email": "maya.chen@example.com",
        "profile": {
            "slug": "maya-chen",
            "role": UserProfile.Role.CLIENT,
            "badge": "Verified homeowner",
            "area": "Notre-Dame-de-Grace",
            "summary": (
                "Posts clear scope, photo references, and flexible evening "
                "pickup windows."
            ),
        },
    },
    {
        "username": "samir.bensaid",
        "first_name": "Samir",
        "last_name": "Ben Said",
        "email": "samir.bensaid@example.com",
        "profile": {
            "slug": "samir-bensaid",
            "role": UserProfile.Role.WORKER,
            "badge": "Transit-ready shoveller",
            "area": "Verdun",
            "summary": (
                "Takes on duplex entrances and stair-heavy jobs within a "
                "30-minute commute."
            ),
        },
    },
    {
        "username": "camille.roy",
        "first_name": "Camille",
        "last_name": "Roy",
        "email": "camille.roy@example.com",
        "profile": {
            "slug": "camille-roy",
            "role": UserProfile.Role.CLIENT,
            "badge": "Repeat poster",
            "area": "LaSalle",
            "summary": (
                "Usually posts morning jobs with driveway photos and same-day "
                "payment."
            ),
        },
    },
    {
        "username": "alejandro.torres",
        "first_name": "Alejandro",
        "last_name": "Torres",
        "email": "alejandro.torres@example.com",
        "profile": {
            "slug": "alejandro-torres",
            "role": UserProfile.Role.WORKER,
            "badge": "Weekend availability",
            "area": "Cote-des-Neiges",
            "summary": (
                "Prefers weekend work near metro stops and can bring his own "
                "salt spreader."
            ),
        },
    },
]

POSTINGS = [
    {
        "slug": "ndg-front-steps",
        "title": "NDG duplex needs front steps and walkway cleared",
        "kind": Posting.Kind.CLIENT_POST,
        "budget": "$55",
        "window": "Tonight after 7:00 PM",
        "location": "Notre-Dame-de-Grace",
        "summary": (
            "Front stairs, short walkway, and one parking strip after the "
            "snowfall slows down."
        ),
        "details": (
            "Salt is already on site. The client added pictures and can "
            "message door access notes before arrival."
        ),
        "areas": ["Front steps", "Walkway", "Parking strip"],
        "account_slug": "maya-chen",
    },
    {
        "slug": "verdun-evening-route",
        "title": "Verdun evening shoveller taking jobs near Jolicoeur",
        "kind": Posting.Kind.WORKER_PROFILE,
        "budget": "From $40 per visit",
        "window": "Available 6:30 PM to 10:30 PM",
        "location": "Verdun",
        "summary": (
            "Best fit for entrances, duplex stairs, and compact driveways "
            "within transit range."
        ),
        "details": (
            "Samir can reach most jobs by bus and metro, and he is comfortable "
            "handling repeat bookings after storms."
        ),
        "areas": ["Entrance", "Stairs", "Compact driveway"],
        "account_slug": "samir-bensaid",
    },
    {
        "slug": "lasalle-morning-driveway",
        "title": "LaSalle driveway and side path needed before 9:00 AM",
        "kind": Posting.Kind.CLIENT_POST,
        "budget": "$70",
        "window": "Tomorrow before 9:00 AM",
        "location": "LaSalle",
        "summary": (
            "Two-car driveway, side path to the bins, and light salting if "
            "the worker can do it."
        ),
        "details": (
            "The account usually posts with photo guides and pays right after "
            "the work is marked complete."
        ),
        "areas": ["Driveway", "Side path", "Bins access"],
        "account_slug": "camille-roy",
    },
    {
        "slug": "cdn-weekend-worker",
        "title": "Weekend worker covering snow clearing near Snowdon",
        "kind": Posting.Kind.WORKER_PROFILE,
        "budget": "From $45 per visit",
        "window": "Friday to Sunday",
        "location": "Cote-des-Neiges",
        "summary": (
            "Open to morning or late-night jobs, especially homes close to "
            "metro stations."
        ),
        "details": (
            "Alejandro brings his own shovel kit and is open to recurring "
            "service for the same address."
        ),
        "areas": ["Entrance", "Walkway", "Salt spread"],
        "account_slug": "alejandro-torres",
    },
]

RATINGS = [
    {
        "reviewer_slug": "maya-chen",
        "reviewee_slug": "samir-bensaid",
        "posting_slug": "ndg-front-steps",
        "score": 5,
        "comment": "Samir arrived on time and did a thorough job on the steps. Would book again.",
    },
    {
        "reviewer_slug": "samir-bensaid",
        "reviewee_slug": "maya-chen",
        "posting_slug": "ndg-front-steps",
        "score": 5,
        "comment": "Clear instructions, salt was ready, and the payment came through fast.",
    },
    {
        "reviewer_slug": "camille-roy",
        "reviewee_slug": "alejandro-torres",
        "posting_slug": "lasalle-morning-driveway",
        "score": 4,
        "comment": "Good work on the driveway. The side path could use a second pass next time.",
    },
    {
        "reviewer_slug": "alejandro-torres",
        "reviewee_slug": "camille-roy",
        "posting_slug": "lasalle-morning-driveway",
        "score": 5,
        "comment": "Photo guide made the job super easy. Paid right away.",
    },
    {
        "reviewer_slug": "maya-chen",
        "reviewee_slug": "alejandro-torres",
        "posting_slug": "cdn-weekend-worker",
        "score": 4,
        "comment": "Reliable weekend option. Brought his own salt spreader which was a nice bonus.",
    },
    {
        "reviewer_slug": "camille-roy",
        "reviewee_slug": "samir-bensaid",
        "posting_slug": "verdun-evening-route",
        "score": 5,
        "comment": "Handled the evening job perfectly. Very professional.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo users, postings, and ratings."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing seed data before re-seeding.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing data …")
            EXIFMetadata.objects.all().delete()
            WorkProof.objects.all().delete()
            Rating.objects.all().delete()
            Posting.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        if UserProfile.objects.exists():
            self.stdout.write(
                self.style.WARNING("Data already exists. Use --flush to re-seed.")
            )
            return

        # ------ Users + Profiles ------
        profiles = {}
        for data in USERS:
            profile_data = data.pop("profile")
            user, _ = User.objects.get_or_create(
                username=data["username"],
                defaults={**data, "password": "!unusable"},
            )
            # Set an unusable password (demo accounts)
            user.set_unusable_password()
            user.save()
            profile = UserProfile.objects.create(user=user, **profile_data)
            profiles[profile.slug] = profile
            self.stdout.write(f"  Created user + profile: {profile}")

        # ------ Postings ------
        posting_map = {}
        for data in POSTINGS:
            account_slug = data.pop("account_slug")
            posting = Posting.objects.create(
                account=profiles[account_slug],
                **data,
            )
            posting_map[posting.slug] = posting
            self.stdout.write(f"  Created posting: {posting}")

        # ------ Ratings ------
        for data in RATINGS:
            Rating.objects.create(
                reviewer=profiles[data["reviewer_slug"]],
                reviewee=profiles[data["reviewee_slug"]],
                posting=posting_map.get(data["posting_slug"]),
                score=data["score"],
                comment=data["comment"],
            )
            self.stdout.write(
                f"  Created rating: {data['reviewer_slug']} → "
                f"{data['reviewee_slug']} ({data['score']}/5)"
            )

        # ------ Work proofs (before / after demo) ------
        before_img = DEMO_IMG_DIR / "before.png"
        after_img = DEMO_IMG_DIR / "after.png"

        proof = None
        if before_img.exists() and after_img.exists():
            ndg_posting = posting_map.get("ndg-front-steps")
            samir = profiles.get("samir-bensaid")
            if ndg_posting and samir:
                proof = WorkProof(posting=ndg_posting, worker=samir, caption="Steps, walkway and parking strip done.")
                with open(before_img, "rb") as bf:
                    proof.photo_before.save("before_ndg.png", File(bf), save=False)
                with open(after_img, "rb") as af:
                    proof.photo_after.save("after_ndg.png", File(af), save=False)
                proof.save()
                self.stdout.write("  Created work proof: Samir → NDG front steps")
        else:
            self.stdout.write(
                self.style.WARNING(
                    "  Skipping work proof — demo images not found. "
                    f"Expected at: {DEMO_IMG_DIR}"
                )
            )

        # ------ EXIF metadata stubs (demo data) ------
        if proof is not None:
            from datetime import datetime, timezone

            exif_base = {
                "camera_make": "Apple",
                "camera_model": "iPhone 15 Pro",
                "software": "iOS 18.2",
                "latitude": 45.4773,
                "longitude": -73.6220,
                "altitude": 36.0,
                "image_width": 4032,
                "image_height": 3024,
                "orientation": 1,
                "raw_exif": {
                    "Make": "Apple",
                    "Model": "iPhone 15 Pro",
                    "Software": "iOS 18.2",
                    "Orientation": 1,
                },
            }

            EXIFMetadata.objects.create(
                work_proof=proof,
                image_field_name="photo_before",
                datetime_original=datetime(2026, 1, 15, 18, 30, 0, tzinfo=timezone.utc),
                **exif_base,
            )
            EXIFMetadata.objects.create(
                work_proof=proof,
                image_field_name="photo_after",
                datetime_original=datetime(2026, 1, 15, 19, 45, 0, tzinfo=timezone.utc),
                **exif_base,
            )
            self.stdout.write("  Created EXIF metadata stubs for work proof")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeded {len(USERS)} users, {len(POSTINGS)} postings, "
                f"{len(RATINGS)} ratings, and work proofs."
            )
        )
