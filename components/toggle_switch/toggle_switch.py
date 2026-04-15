from django_components import Component, register

@register("toggle_switch")
class ToggleSwitch(Component):
    template_name = "toggle_switch/toggle_switch.html"

    def get_context_data(self, label_on, label_off, id=None, onclick=None):
        return {
            "label_on": label_on,
            "label_off": label_off,
            "id": id,
            "onclick": onclick,
        }

    class Media:
        css = {"all": ["toggle_switch/toggle_switch.css"]}
