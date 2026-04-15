from django_components import Component, register

@register("stack")
class Stack(Component):
    template_name = "stack/stack.html"

    def get_context_data(self, gap="1rem"):
        return {"gap": gap}

    class Media:
        css = {"all": ["stack/stack.css"]}
