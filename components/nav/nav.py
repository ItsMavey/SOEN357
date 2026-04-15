from django_components import Component, register


@register("nav")
class Nav(Component):
    template_name = "nav/nav.html"

    def get_context_data(self, brand="Snow", subtitle=""):
        return {
            "brand": brand,
            "subtitle": subtitle,
        }

    class Media:
        css = {"all": ["nav/nav.css"]}
