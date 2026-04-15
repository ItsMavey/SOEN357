from django_components import Component, register

@register("button")
class Button(Component):
    template_name = "button/button.html"

    def get_context_data(self, label, href=None, tone=None, type="button", **attrs):
        return {
            "label": label,
            "href": href,
            "tone": tone,
            "type": type,
            "attrs": attrs,
        }

    class Media:
        css = {"all": ["button/button.css"]}
