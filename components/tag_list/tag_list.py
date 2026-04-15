from django_components import Component, register

@register("tag_list")
class TagList(Component):
    template_name = "tag_list/tag_list.html"

    def get_context_data(self, tags):
        return {"tags": tags}

    class Media:
        css = {"all": ["tag_list/tag_list.css"]}
