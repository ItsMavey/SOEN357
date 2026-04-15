from django_components import Component, register

@register("form_group")
class FormGroup(Component):
    template_name = "form_group/form_group.html"

    def get_context_data(self, title):
        return {"title": title}

    class Media:
        css = {"all": ["form_group/form_group.css"]}
