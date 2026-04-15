from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_page_renders_preferences_screen(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Set up your experience before you continue")
        self.assertContains(response, "Themes / colors")

    def test_flow_pages_render(self):
        for route_name in [
            "login",
            "signup",
            "worker_registration",
            "property_form",
            "postings",
            "profile_settings",
            "themes",
            "languages",
        ]:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200)

    def test_posting_and_account_detail_pages_render(self):
        posting_response = self.client.get(reverse("posting_detail", args=["ndg-front-steps"]))
        account_response = self.client.get(reverse("account_detail", args=["maya-chen"]))

        self.assertEqual(posting_response.status_code, 200)
        self.assertEqual(account_response.status_code, 200)
        self.assertContains(posting_response, "Maya Chen")
        self.assertContains(account_response, "NDG duplex needs front steps and walkway cleared")

    def test_home_contains_real_navigation_targets(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("login"))
        self.assertContains(response, reverse("signup"))
        self.assertContains(response, reverse("themes"))
        self.assertContains(response, reverse("languages"))

    def test_signup_links_to_both_follow_up_flows(self):
        response = self.client.get(reverse("signup"))

        self.assertContains(response, reverse("worker_registration"))
        self.assertContains(response, reverse("property_form"))

    def test_french_translation_appears_in_nav_and_screen(self):
        response = self.client.get(reverse("signup"), HTTP_ACCEPT_LANGUAGE="fr")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creation du compte")
        self.assertContains(response, "Connexion")

    def test_postings_page_uses_real_accounts(self):
        response = self.client.get(reverse("postings"))

        self.assertContains(response, "Maya Chen")
        self.assertContains(response, reverse("account_detail", args=["maya-chen"]))
        self.assertContains(response, reverse("posting_detail", args=["ndg-front-steps"]))

    def test_french_postings_translation_appears_on_detail_actions(self):
        response = self.client.get(reverse("postings"), HTTP_ACCEPT_LANGUAGE="fr")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Secteur")
        self.assertContains(response, "Ouvrir les details")
