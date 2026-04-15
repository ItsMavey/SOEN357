from django_components import Component, register

@register("upload_field")
class UploadField(Component):
    template_name = "upload_field/upload_field.html"

    def get_context_data(self, label, name=None):
        return {"label": label, "name": name}

    class Media:
        css = {"all": ["upload_field/upload_field.css"]}
