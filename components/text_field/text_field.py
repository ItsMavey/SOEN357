from django_components import Component, register

@register("text_field")
class TextField(Component):
    template_name = "text_field/text_field.html"

    def get_context_data(self, label, name=None, type="text", placeholder=None, value=None, **attrs):
        return {
            "label": label,
            "name": name,
            "type": type,
            "placeholder": placeholder,
            "value": value,
            "attrs": attrs,
        }

    class Media:
        css = {"all": ["text_field/text_field.css"]}
