from django_components import Component, register

@register("posting_card")
class PostingCard(Component):
    template_name = "posting_card/posting_card.html"

    def get_context_data(self, posting):
        return {
            "posting": posting,
        }

    class Media:
        css = {"all": ["posting_card/posting_card.css"]}
