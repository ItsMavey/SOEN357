from django_components import Component, register

@register("fact_grid")
class FactGrid(Component):
    template_name = "fact_grid/fact_grid.html"

    def get_context_data(self, variant=None):
        return {"variant": variant}

    class Media:
        css = {"all": ["fact_grid/fact_grid.css"]}
