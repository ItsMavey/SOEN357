from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


def get_accounts():
    return {
        "maya-chen": {
            "slug": "maya-chen",
            "name": "Maya Chen",
            "role": _("Client"),
            "badge": _("Verified homeowner"),
            "area": _("Notre-Dame-de-Grace"),
            "summary": _(
                "Posts clear scope, photo references, and flexible evening pickup windows."
            ),
        },
        "samir-bensaid": {
            "slug": "samir-bensaid",
            "name": "Samir Ben Said",
            "role": _("Worker"),
            "badge": _("Transit-ready shoveller"),
            "area": _("Verdun"),
            "summary": _(
                "Takes on duplex entrances and stair-heavy jobs within a 30-minute commute."
            ),
        },
        "camille-roy": {
            "slug": "camille-roy",
            "name": "Camille Roy",
            "role": _("Client"),
            "badge": _("Repeat poster"),
            "area": _("LaSalle"),
            "summary": _(
                "Usually posts morning jobs with driveway photos and same-day payment."
            ),
        },
        "alejandro-torres": {
            "slug": "alejandro-torres",
            "name": "Alejandro Torres",
            "role": _("Worker"),
            "badge": _("Weekend availability"),
            "area": _("Cote-des-Neiges"),
            "summary": _(
                "Prefers weekend work near metro stops and can bring his own salt spreader."
            ),
        },
    }


def get_postings():
    accounts = get_accounts()
    postings = [
        {
            "slug": "ndg-front-steps",
            "title": _("NDG duplex needs front steps and walkway cleared"),
            "kind": _("Client post"),
            "budget": "$55",
            "window": _("Tonight after 7:00 PM"),
            "location": _("Notre-Dame-de-Grace"),
            "summary": _(
                "Front stairs, short walkway, and one parking strip after the snowfall slows down."
            ),
            "details": _(
                "Salt is already on site. The client added pictures and can message door access notes before arrival."
            ),
            "areas": [_("Front steps"), _("Walkway"), _("Parking strip")],
            "account": accounts["maya-chen"],
        },
        {
            "slug": "verdun-evening-route",
            "title": _("Verdun evening shoveller taking jobs near Jolicoeur"),
            "kind": _("Worker profile"),
            "budget": _("From $40 per visit"),
            "window": _("Available 6:30 PM to 10:30 PM"),
            "location": _("Verdun"),
            "summary": _(
                "Best fit for entrances, duplex stairs, and compact driveways within transit range."
            ),
            "details": _(
                "Samir can reach most jobs by bus and metro, and he is comfortable handling repeat bookings after storms."
            ),
            "areas": [_("Entrance"), _("Stairs"), _("Compact driveway")],
            "account": accounts["samir-bensaid"],
        },
        {
            "slug": "lasalle-morning-driveway",
            "title": _("LaSalle driveway and side path needed before 9:00 AM"),
            "kind": _("Client post"),
            "budget": "$70",
            "window": _("Tomorrow before 9:00 AM"),
            "location": _("LaSalle"),
            "summary": _(
                "Two-car driveway, side path to the bins, and light salting if the worker can do it."
            ),
            "details": _(
                "The account usually posts with photo guides and pays right after the work is marked complete."
            ),
            "areas": [_("Driveway"), _("Side path"), _("Bins access")],
            "account": accounts["camille-roy"],
        },
        {
            "slug": "cdn-weekend-worker",
            "title": _("Weekend worker covering snow clearing near Snowdon"),
            "kind": _("Worker profile"),
            "budget": _("From $45 per visit"),
            "window": _("Friday to Sunday"),
            "location": _("Cote-des-Neiges"),
            "summary": _(
                "Open to morning or late-night jobs, especially homes close to metro stations."
            ),
            "details": _(
                "Alejandro brings his own shovel kit and is open to recurring service for the same address."
            ),
            "areas": [_("Entrance"), _("Walkway"), _("Salt spread")],
            "account": accounts["alejandro-torres"],
        },
    ]

    return postings


class NavContextMixin:
    nav_brand = "Bing Chilling"
    nav_page_title = _("Neighbours shovelling services")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("nav_brand", self.nav_brand)
        context.setdefault("nav_page_title", self.nav_page_title)
        return context


class HomeView(NavContextMixin, TemplateView):
    template_name = "home.html"
    nav_page_title = _("Neighbours shovelling services")


class LoginView(NavContextMixin, TemplateView):
    template_name = "info_page.html"
    nav_page_title = _("Login")
    extra_context = {
        "page_eyebrow": _("Account"),
        "page_title": _("Login"),
        "page_description": _(
            "Returning users will be able to access their dashboard, saved preferences, and active posts from here."
        ),
        "primary_url_name": "postings",
        "primary_label": _("Go to postings"),
    }


class SignupView(NavContextMixin, TemplateView):
    template_name = "account_creation.html"
    nav_page_title = _("Account creation")


class WorkerRegistrationView(NavContextMixin, TemplateView):
    template_name = "worker_registration.html"
    nav_page_title = _("Shoveller registration")


class PropertyFormView(NavContextMixin, TemplateView):
    template_name = "property_form.html"
    nav_page_title = _("New property form")


class PostingsView(NavContextMixin, TemplateView):
    template_name = "postings.html"
    nav_page_title = _("Postings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postings"] = get_postings()
        return context


class PostingDetailView(NavContextMixin, TemplateView):
    template_name = "posting_detail.html"
    nav_page_title = _("Postings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posting = next(
            (item for item in get_postings() if item["slug"] == self.kwargs["slug"]),
            None,
        )
        if posting is None:
            raise Http404(_("Posting not found."))

        context["posting"] = posting
        context["nav_page_title"] = posting["title"]
        return context


class AccountDetailView(NavContextMixin, TemplateView):
    template_name = "account_profile.html"
    nav_page_title = _("Profile and settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = get_accounts().get(self.kwargs["slug"])
        if account is None:
            raise Http404(_("Account not found."))

        account_postings = [
            item for item in get_postings() if item["account"]["slug"] == account["slug"]
        ]

        context["account"] = account
        context["account_postings"] = account_postings
        context["nav_page_title"] = account["name"]
        return context


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
