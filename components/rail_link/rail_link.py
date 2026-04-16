from django_components import Component, register

@register("rail_link")
class RailLink(Component):
    template_name = "rail_link/rail_link.html"

    def get_context_data(self, url="#", eyebrow=None, title="Link", body=None, arrow=False, tone=None, stretch=False, **attrs):
        return {
            "url": url,
            "eyebrow": eyebrow,
            "title": title,
            "body": body,
            "arrow": arrow,
            "tone": tone,
            "stretch": stretch,
            "attrs": {k.replace("_", "-"): v for k, v in attrs.items()},
        }

    class Media:
        css = {"all": ["rail_link/rail_link.css"]}
