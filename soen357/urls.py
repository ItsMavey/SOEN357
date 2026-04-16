from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Snow.views import (
    AccountDetailView,
    HomeView,
    LanguagesView,
    LoginView,
    LogoutView,
    MarkCompletedView,
    PostingDetailView,
    PostingsView,
    ProfileSettingsView,
    PropertyFormView,
    SignupView,
    ThemesView,
    WorkerRegistrationView,
    WorkProofUploadView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("worker-registration/", WorkerRegistrationView.as_view(), name="worker_registration"),
    path("property-form/", PropertyFormView.as_view(), name="property_form"),
    path("postings/", PostingsView.as_view(), name="postings"),
    path("postings/<slug:slug>/", PostingDetailView.as_view(), name="posting_detail"),
    path("postings/<slug:slug>/upload-proof/", WorkProofUploadView.as_view(), name="upload_work_proof"),
    path("postings/<slug:slug>/mark-completed/", MarkCompletedView.as_view(), name="mark_completed"),
    path("accounts/<slug:slug>/", AccountDetailView.as_view(), name="account_detail"),
    path("profile-settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("themes/", ThemesView.as_view(), name="themes"),
    path("languages/", LanguagesView.as_view(), name="languages"),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
