from django_components import Component, register

@register("surface")
class Surface(Component):
    template_name = "surface/surface.html"

    def get_context_data(self, kind="panel", flow=None):
        return {"kind": kind, "flow": flow}

    class Media:
        css = {"all": ["surface/surface.css"]}
