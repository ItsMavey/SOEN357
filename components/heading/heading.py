from django_components import Component, register

@register("heading")
class Heading(Component):
    template_name = "heading/heading.html"

    def get_context_data(self, title, support=None, eyebrow=None, level=2, compact=False):
        return {
            "title": title,
            "support": support,
            "eyebrow": eyebrow,
            "level": level,
            "compact": compact,
        }

    class Media:
        css = {"all": ["heading/heading.css"]}
