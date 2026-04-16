from django_components import Component, register

@register("button_tile")
class ButtonTile(Component):
    template_name = "button_tile/button_tile.html"

    def get_context_data(self, label, href, tone=None):
        return {"label": label, "href": href, "tone": tone}

    class Media:
        css = {"all": ["button_tile/button_tile.css"]}
