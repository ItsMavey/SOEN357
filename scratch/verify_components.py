import os
import django
from django.conf import settings
from django.template import Template, Context

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soen357.settings')
django.setup()

def test_render_rail_link():
    t = Template("{% load component_tags %}{% component 'rail_link' url='/test' title='Test Link' / %}")
    c = Context({})
    print("Testing RailLink:")
    print(t.render(c))
    print("-" * 20)

def test_render_posting_card():
    posting = {
        "title": "Snow Shoveling Job",
        "kind": "Client post",
        "budget": "$50",
        "location": "Verdun",
        "window": "Tomorrow",
        "summary": "Need help clearing driveway.",
        "account": {"slug": "test-user", "name": "John Doe", "badge": "Verified", "area": "Verdun"},
        "slug": "snow-job"
    }
    t = Template("{% load component_tags %}{% component 'posting_card' posting=posting / %}")
    c = Context({"posting": posting})
    print("Testing PostingCard:")
    print(t.render(c))
    print("-" * 20)

if __name__ == "__main__":
    test_render_rail_link()
    test_render_posting_card()
