from django_components import Component, register

@register("segment_control")
class SegmentControl(Component):
    template_name = "segment_control/segment_control.html"

    def get_context_data(self, label):
        return {"label": label}

    class Media:
        css = {"all": ["segment_control/segment_control.css"]}
