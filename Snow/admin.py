from django.contrib import admin

from .models import EXIFMetadata, Posting, Rating, UserProfile, WorkProof


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "role", "area", "badge")
    list_filter = ("role",)
    search_fields = ("user__first_name", "user__last_name", "slug", "area")
    prepopulated_fields = {"slug": ("user",)}


@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "budget", "location", "account", "created_at")
    list_filter = ("kind", "location")
    search_fields = ("title", "location", "account__user__first_name")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "reviewee", "score", "posting", "created_at")
    list_filter = ("score",)
    search_fields = (
        "reviewer__user__first_name",
        "reviewee__user__first_name",
        "comment",
    )


class EXIFMetadataInline(admin.TabularInline):
    model = EXIFMetadata
    extra = 0
    readonly_fields = (
        "image_field_name",
        "latitude",
        "longitude",
        "altitude",
        "camera_make",
        "camera_model",
        "datetime_original",
        "orientation",
        "software",
        "image_width",
        "image_height",
    )


@admin.register(WorkProof)
class WorkProofAdmin(admin.ModelAdmin):
    list_display = ("posting", "worker", "caption", "created_at")
    list_filter = ("worker",)
    search_fields = ("posting__title", "worker__user__first_name", "caption")
    inlines = [EXIFMetadataInline]


@admin.register(EXIFMetadata)
class EXIFMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "work_proof",
        "image_field_name",
        "camera_make",
        "camera_model",
        "datetime_original",
        "latitude",
        "longitude",
    )
    list_filter = ("camera_make", "image_field_name")
    search_fields = ("work_proof__posting__title", "camera_make", "camera_model")
    readonly_fields = ("raw_exif",)
