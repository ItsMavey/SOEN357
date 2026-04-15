from django_components import Component, register

@register("grid")
class Grid(Component):
    template_name = "grid/grid.html"

    def get_context_data(self, variant=None):
        return {"variant": variant}

    class Media:
        css = {"all": ["grid/grid.css"]}
