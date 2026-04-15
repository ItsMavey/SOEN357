from django.contrib import admin
from django.urls import include, path

from Snow.views import (
    AccountDetailView,
    HomeView,
    LanguagesView,
    LoginView,
    PostingDetailView,
    PostingsView,
    ProfileSettingsView,
    PropertyFormView,
    SignupView,
    ThemesView,
    WorkerRegistrationView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("worker-registration/", WorkerRegistrationView.as_view(), name="worker_registration"),
    path("property-form/", PropertyFormView.as_view(), name="property_form"),
    path("postings/", PostingsView.as_view(), name="postings"),
    path("postings/<slug:slug>/", PostingDetailView.as_view(), name="posting_detail"),
    path("accounts/<slug:slug>/", AccountDetailView.as_view(), name="account_detail"),
    path("profile-settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("themes/", ThemesView.as_view(), name="themes"),
    path("languages/", LanguagesView.as_view(), name="languages"),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]
