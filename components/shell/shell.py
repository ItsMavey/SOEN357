from django_components import Component, register

@register("shell")
class Shell(Component):
    template_name = "shell/shell.html"

    def get_context_data(self, layout="page", variant=None, **kwargs):
        # Inspecting kwargs to see what django-components passes
        return {
            "layout": layout,
            "variant": variant,
            "has_rail_left": "rail_left" in self.slots,
            "has_sidebar": "sidebar" in self.slots,
            "has_rail_right": "rail_right" in self.slots,
            "has_default": "default" in self.slots,
        }

    class Media:
        css = {"all": ["shell/shell.css"]}
