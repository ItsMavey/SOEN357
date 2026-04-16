from django_components import Component, register

@register("choice_card")
class ChoiceCard(Component):
    template_name = "choice_card/choice_card.html"

    def get_context_data(self, title=None, support=None, value=None, name=None, href=None, selected=False, tone=None, type="submit", **attrs):
        if "data_ui" not in attrs:
            attrs["data_ui"] = "choice"

        return {
            "title": title,
            "support": support,
            "value": value,
            "name": name,
            "href": href,
            "selected": selected,
            "tone": tone,
            "type": type,
            "attrs": {k.replace("_", "-"): v for k, v in attrs.items()},
        }

    class Media:
        css = {"all": ["choice_card/choice_card.css"]}
