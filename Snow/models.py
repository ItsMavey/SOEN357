from django.conf import settings
from django.db import models
from django.utils.text import slugify


class UserProfile(models.Model):
    """Extended profile attached to each Django User."""

    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        WORKER = "worker", "Worker"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    badge = models.CharField(max_length=120, blank=True)
    area = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = self.user.get_full_name() or self.user.username
            self.slug = slugify(full_name)
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        """Return the average score from all received ratings, or None."""
        from django.db.models import Avg

        result = self.ratings_received.aggregate(avg=Avg("score"))
        return round(result["avg"], 1) if result["avg"] is not None else None

    @property
    def rating_count(self):
        """Return the total number of received ratings."""
        return self.ratings_received.count()

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"


class Posting(models.Model):
    """A snow-clearing posting — either a client request or a worker profile."""

    class Kind(models.TextChoices):
        CLIENT_POST = "client_post", "Client post"
        WORKER_PROFILE = "worker_profile", "Worker profile"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"

    slug = models.SlugField(max_length=160, unique=True, blank=True)
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=20, choices=Kind.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN,
    )
    budget = models.CharField(max_length=60)
    window = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    details = models.TextField(blank=True)
    areas = models.JSONField(default=list, blank=True)
    account = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="postings",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Rating(models.Model):
    """A rating left by one user on another user's profile."""

    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="ratings_given",
    )
    reviewee = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="ratings_received",
    )
    posting = models.ForeignKey(
        Posting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ratings",
    )
    score = models.PositiveSmallIntegerField(
        help_text="Rating from 1 to 5",
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "reviewee", "posting")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer} → {self.reviewee}: {self.score}/5"


class WorkProof(models.Model):
    """Before-and-after photo proof submitted by a worker for a posting."""

    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE,
        related_name="work_proofs",
    )
    worker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="work_proofs",
        limit_choices_to={"role": "worker"},
    )
    photo_before = models.ImageField(upload_to="work_proofs/before/")
    photo_after = models.ImageField(upload_to="work_proofs/after/")
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        worker_name = self.worker.user.get_full_name() or self.worker.user.username
        return f"Proof by {worker_name} for {self.posting.title}"


class EXIFMetadata(models.Model):
    """EXIF data extracted from a WorkProof image."""

    IMAGE_FIELD_CHOICES = [
        ("photo_before", "Before photo"),
        ("photo_after", "After photo"),
    ]

    work_proof = models.ForeignKey(
        WorkProof,
        on_delete=models.CASCADE,
        related_name="exif_entries",
    )
    image_field_name = models.CharField(
        max_length=20,
        choices=IMAGE_FIELD_CHOICES,
        help_text="Which image this EXIF data belongs to.",
    )

    # GPS
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(
        null=True, blank=True, help_text="Altitude in metres."
    )

    # Camera
    camera_make = models.CharField(max_length=120, blank=True)
    camera_model = models.CharField(max_length=120, blank=True)

    # Timestamp
    datetime_original = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date/time the photo was originally taken.",
    )

    # Technical
    orientation = models.PositiveSmallIntegerField(null=True, blank=True)
    software = models.CharField(max_length=200, blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)

    # Raw dump for future use
    raw_exif = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "EXIF metadata"
        verbose_name_plural = "EXIF metadata"
        unique_together = ("work_proof", "image_field_name")

    def __str__(self):
        return f"EXIF ({self.image_field_name}) — {self.work_proof}"

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _dms_to_decimal(dms, ref):
        """Convert EXIF GPS DMS tuple to a decimal float."""
        try:
            degrees = float(dms[0])
            minutes = float(dms[1])
            seconds = float(dms[2])
            decimal = degrees + minutes / 60.0 + seconds / 3600.0
            if ref in ("S", "W"):
                decimal = -decimal
            return round(decimal, 7)
        except (TypeError, IndexError, ValueError):
            return None

    @classmethod
    def extract_from_image(cls, image_field):
        """
        Open an ImageField file, read EXIF tags with Pillow, and return a
        dict of parsed values.  Returns an empty dict when no EXIF is found.
        """
        import json
        import logging
        from datetime import datetime

        from PIL import Image
        from PIL.ExifTags import GPSTAGS, TAGS

        logger = logging.getLogger(__name__)
        result = {}

        try:
            image_field.open("rb")
            img = Image.open(image_field)
            exif_data = img._getexif()
            if exif_data is None:
                return result

            # Build human-readable tag dict
            readable = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                # Skip binary / non-serialisable blobs
                try:
                    json.dumps(value)
                    readable[str(tag_name)] = value
                except (TypeError, ValueError):
                    readable[str(tag_name)] = str(value)

            result["raw_exif"] = readable
            result["camera_make"] = str(readable.get("Make", "")).strip()
            result["camera_model"] = str(readable.get("Model", "")).strip()
            result["software"] = str(readable.get("Software", "")).strip()
            result["orientation"] = readable.get("Orientation")

            # Dimensions
            result["image_width"] = readable.get(
                "ExifImageWidth"
            ) or readable.get("ImageWidth")
            result["image_height"] = readable.get(
                "ExifImageHeight"
            ) or readable.get("ImageLength")

            # Original datetime
            dt_str = readable.get("DateTimeOriginal") or readable.get(
                "DateTime"
            )
            if dt_str:
                for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                    try:
                        result["datetime_original"] = datetime.strptime(
                            dt_str, fmt
                        )
                        break
                    except ValueError:
                        continue

            # GPS
            gps_info = exif_data.get(34853)  # GPSInfo tag
            if gps_info:
                gps_data = {}
                for gps_tag_id, gps_value in gps_info.items():
                    gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag_name] = gps_value

                lat_dms = gps_data.get("GPSLatitude")
                lat_ref = gps_data.get("GPSLatitudeRef")
                lon_dms = gps_data.get("GPSLongitude")
                lon_ref = gps_data.get("GPSLongitudeRef")

                if lat_dms and lat_ref:
                    result["latitude"] = cls._dms_to_decimal(lat_dms, lat_ref)
                if lon_dms and lon_ref:
                    result["longitude"] = cls._dms_to_decimal(
                        lon_dms, lon_ref
                    )

                alt = gps_data.get("GPSAltitude")
                if alt is not None:
                    try:
                        result["altitude"] = float(alt)
                    except (TypeError, ValueError):
                        pass

        except Exception as exc:  # noqa: BLE001
            logger.warning("EXIF extraction failed: %s", exc)
        finally:
            try:
                image_field.close()
            except Exception:  # noqa: BLE001
                pass

        return result

    @classmethod
    def extract_and_save(cls, work_proof, field_name):
        """
        Extract EXIF from the given field name on a WorkProof and persist it.
        """
        image_field = getattr(work_proof, field_name, None)
        if not image_field:
            return None

        data = cls.extract_from_image(image_field)
        if not data:
            # Create a minimal record so we know extraction was attempted
            return cls.objects.create(
                work_proof=work_proof,
                image_field_name=field_name,
            )

        return cls.objects.create(
            work_proof=work_proof,
            image_field_name=field_name,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude"),
            camera_make=data.get("camera_make", ""),
            camera_model=data.get("camera_model", ""),
            datetime_original=data.get("datetime_original"),
            orientation=data.get("orientation"),
            software=data.get("software", ""),
            image_width=data.get("image_width"),
            image_height=data.get("image_height"),
            raw_exif=data.get("raw_exif", {}),
        )
