from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import Http404
from django.shortcuts import redirect
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .models import EXIFMetadata, Posting, UserProfile, WorkProof

User = get_user_model()


# ---------------------------------------------------------------------------
# Shared mixin
# ---------------------------------------------------------------------------

class NavContextMixin:
    nav_brand = "Bing Chilling"
    nav_page_title = _("Neighbours shovelling services")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("nav_brand", self.nav_brand)
        context.setdefault("nav_page_title", self.nav_page_title)
        return context


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

class HomeView(NavContextMixin, TemplateView):
    template_name = "home.html"
    nav_page_title = _("Neighbours shovelling services")


# ---------------------------------------------------------------------------
# Auth — Login
# ---------------------------------------------------------------------------

class LoginView(NavContextMixin, TemplateView):
    template_name = "login.html"
    nav_page_title = _("Login")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("postings")

        context = self.get_context_data()
        context["form_error"] = _("Invalid username or password.")
        context["form_username"] = username
        return self.render_to_response(context)


# ---------------------------------------------------------------------------
# Auth — Signup
# ---------------------------------------------------------------------------

class SignupView(NavContextMixin, TemplateView):
    template_name = "account_creation.html"
    nav_page_title = _("Account creation")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        role = request.POST.get("role", "worker")

        errors = []

        if not username:
            errors.append(_("Username is required."))
        if not email:
            errors.append(_("Email is required."))
        if not password:
            errors.append(_("Password is required."))
        if password != password_confirm:
            errors.append(_("Passwords do not match."))
        if User.objects.filter(username=username).exists():
            errors.append(_("That username is already taken."))

        if errors:
            context = self.get_context_data()
            context["form_errors"] = errors
            context["form_username"] = username
            context["form_email"] = email
            context["form_phone"] = phone
            context["form_role"] = role
            return self.render_to_response(context)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        profile_role = (
            UserProfile.Role.WORKER if role == "worker" else UserProfile.Role.CLIENT
        )
        UserProfile.objects.create(
            user=user,
            slug=slugify(username),
            role=profile_role,
        )
        auth_login(request, user)

        if profile_role == UserProfile.Role.WORKER:
            return redirect("worker_registration")
        return redirect("property_form")


# ---------------------------------------------------------------------------
# Auth — Logout
# ---------------------------------------------------------------------------

class LogoutView(NavContextMixin, TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect("home")


# ---------------------------------------------------------------------------
# Worker registration
# ---------------------------------------------------------------------------

class WorkerRegistrationView(NavContextMixin, TemplateView):
    template_name = "worker_registration.html"
    nav_page_title = _("Shoveller registration")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        profile = request.user.profile
        profile.area = request.POST.get("address", "").strip()
        profile.badge = _("Transit-ready shoveller")
        profile.summary = (
            f"Range: {request.POST.get('range_km', '')} km, "
            f"Max commute: {request.POST.get('commute', '')}"
        )
        profile.save()
        return redirect("postings")


# ---------------------------------------------------------------------------
# Property form — create a posting
# ---------------------------------------------------------------------------

class PropertyFormView(NavContextMixin, TemplateView):
    template_name = "property_form.html"
    nav_page_title = _("New property form")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        # Collect area checkboxes
        areas = []
        for area_name in ["entrance", "stairs", "garage", "other"]:
            if request.POST.get(f"area_{area_name}"):
                areas.append(area_name.capitalize())
        custom_areas = request.POST.get("areas_custom", "").strip()
        if custom_areas:
            areas.extend([a.strip() for a in custom_areas.split(",") if a.strip()])

        # Collect extras
        extras = []
        if request.POST.get("salt"):
            extras.append("Spread salt or sand")
        other_request = request.POST.get("other_request", "").strip()
        if other_request:
            extras.append(other_request)

        # Timing
        start_time = request.POST.get("start_time", "")
        deadline = request.POST.get("deadline", "")
        when_snow_stops = request.POST.get("when_snow_stops", "")
        tomorrow = request.POST.get("tomorrow", "")

        window_parts = []
        if when_snow_stops:
            window_parts.append(str(_("When snow stops")))
        if start_time:
            window_parts.append(f"Start: {start_time}")
        if tomorrow:
            window_parts.append(str(_("Deadline: Tomorrow")))
        if deadline:
            window_parts.append(f"Deadline: {deadline}")
        window = ", ".join(window_parts) if window_parts else str(_("Flexible"))

        pay = request.POST.get("pay", "").strip()
        address = request.POST.get("address", "").strip()

        title = f"Snow clearing at {address}" if address else str(
            _("New snow clearing post")
        )

        Posting.objects.create(
            title=title,
            kind=Posting.Kind.CLIENT_POST,
            budget=f"${pay}" if pay else str(_("Negotiable")),
            window=window,
            location=address or str(_("Not specified")),
            summary=f"Areas: {', '.join(areas)}" if areas else "",
            details="; ".join(extras) if extras else "",
            areas=areas,
            account=request.user.profile,
        )
        return redirect("postings")


# ---------------------------------------------------------------------------
# Postings list — with filtering
# ---------------------------------------------------------------------------

class PostingsView(NavContextMixin, TemplateView):
    template_name = "postings.html"
    nav_page_title = _("Postings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Posting.objects.select_related("account__user").order_by("-created_at")

        # --- GET-param filtering ---
        params = self.request.GET

        price_min = params.get("price_min", "").strip()
        price_max = params.get("price_max", "").strip()
        start_time = params.get("start_time", "").strip()
        end_time = params.get("end_time", "").strip()
        area_type = params.get("area_type", "").strip()
        extra = params.get("extra", "").strip()

        if price_min:
            try:
                min_val = int(price_min)
                # Filter out postings whose numeric budget is below min
                exclude_ids = []
                for p in qs:
                    numeric = "".join(c for c in p.budget if c.isdigit())
                    if numeric and int(numeric) < min_val:
                        exclude_ids.append(p.pk)
                qs = qs.exclude(pk__in=exclude_ids)
            except ValueError:
                pass
        if price_max:
            try:
                max_val = int(price_max)
                exclude_ids = []
                for p in qs:
                    numeric = "".join(c for c in p.budget if c.isdigit())
                    if numeric and int(numeric) > max_val:
                        exclude_ids.append(p.pk)
                qs = qs.exclude(pk__in=exclude_ids)
            except ValueError:
                pass
        if area_type and area_type != str(_("Any area")):
            # Use icontains on the text representation for SQLite compat
            qs = qs.filter(areas__icontains=area_type)
        if extra:
            qs = qs.filter(details__icontains=extra)

        context["postings"] = qs
        context["filter_price_min"] = price_min
        context["filter_price_max"] = price_max
        context["filter_start_time"] = start_time
        context["filter_end_time"] = end_time
        context["filter_area_type"] = area_type
        context["filter_extra"] = extra
        return context


# ---------------------------------------------------------------------------
# Posting detail
# ---------------------------------------------------------------------------

class PostingDetailView(NavContextMixin, TemplateView):
    template_name = "posting_detail.html"
    nav_page_title = _("Postings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            posting = Posting.objects.select_related("account__user").get(
                slug=self.kwargs["slug"]
            )
        except Posting.DoesNotExist:
            raise Http404(_("Posting not found."))

        context["posting"] = posting
        context["nav_page_title"] = posting.title
        context["work_proofs"] = posting.work_proofs.select_related("worker__user")

        # Show upload form only if logged-in user is authenticated
        context["can_upload_proof"] = self.request.user.is_authenticated
        return context


# ---------------------------------------------------------------------------
# Account detail
# ---------------------------------------------------------------------------

class AccountDetailView(NavContextMixin, TemplateView):
    template_name = "account_profile.html"
    nav_page_title = _("Profile and settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            account = UserProfile.objects.select_related("user").get(
                slug=self.kwargs["slug"]
            )
        except UserProfile.DoesNotExist:
            raise Http404(_("Account not found."))

        account_postings = Posting.objects.filter(account=account).order_by(
            "-created_at"
        )

        context["account"] = account
        context["account_postings"] = account_postings
        context["nav_page_title"] = account.user.get_full_name() or account.user.username
        return context


# ---------------------------------------------------------------------------
# Static info-page views
# ---------------------------------------------------------------------------

class ProfileSettingsView(NavContextMixin, TemplateView):
    template_name = "info_page.html"
    nav_page_title = _("Profile and settings")
    extra_context = {
        "page_eyebrow": _("Profile"),
        "page_title": _("Profile and settings"),
        "page_description": _(
            "Use this area for account details, notification preferences, payment methods, and saved accessibility settings."
        ),
        "primary_url_name": "postings",
        "primary_label": _("Back to postings"),
    }


class ThemesView(NavContextMixin, TemplateView):
    template_name = "info_page.html"
    nav_page_title = _("Themes")
    extra_context = {
        "page_eyebrow": _("Themes"),
        "page_title": _("More themes will live here"),
        "page_description": _(
            "Use this page for additional color systems, accessibility presets, or saved user themes."
        ),
        "primary_url_name": "home",
        "primary_label": _("Back to preferences"),
    }


class LanguagesView(NavContextMixin, TemplateView):
    template_name = "info_page.html"
    nav_page_title = _("Languages")
    extra_context = {
        "page_eyebrow": _("Languages"),
        "page_title": _("More languages page"),
        "page_description": _(
            "Arabic, Italian, and future languages can be managed here when you are ready to add them."
        ),
        "primary_url_name": "home",
        "primary_label": _("Back to preferences"),
    }


# ---------------------------------------------------------------------------
# Work proof upload (logged-in users)
# ---------------------------------------------------------------------------

class WorkProofUploadView(NavContextMixin, TemplateView):
    template_name = "posting_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            posting = Posting.objects.select_related("account__user").get(
                slug=self.kwargs["slug"]
            )
        except Posting.DoesNotExist:
            raise Http404(_("Posting not found."))

        context["posting"] = posting
        context["nav_page_title"] = posting.title
        context["work_proofs"] = posting.work_proofs.select_related("worker__user")
        context["can_upload_proof"] = self.request.user.is_authenticated
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        try:
            posting = Posting.objects.get(slug=self.kwargs["slug"])
        except Posting.DoesNotExist:
            raise Http404(_("Posting not found."))

        photo_before = request.FILES.get("photo_before")
        photo_after = request.FILES.get("photo_after")
        caption = request.POST.get("caption", "").strip()

        if photo_before and photo_after:
            proof = WorkProof.objects.create(
                posting=posting,
                worker=request.user.profile,
                photo_before=photo_before,
                photo_after=photo_after,
                caption=caption,
            )
            # Extract and persist EXIF metadata from both images
            EXIFMetadata.extract_and_save(proof, "photo_before")
            EXIFMetadata.extract_and_save(proof, "photo_after")

        return redirect("posting_detail", slug=posting.slug)


# ---------------------------------------------------------------------------
# Mark posting as completed
# ---------------------------------------------------------------------------

class MarkCompletedView(NavContextMixin, TemplateView):
    template_name = "posting_detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        try:
            posting = Posting.objects.get(slug=self.kwargs["slug"])
        except Posting.DoesNotExist:
            raise Http404(_("Posting not found."))

        # Anyone authenticated can mark as done
        posting.status = Posting.Status.COMPLETED
        posting.save(update_fields=["status"])

        return redirect("posting_detail", slug=posting.slug)
