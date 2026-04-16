from django_components import Component, register


@register("rating_badge")
class RatingBadge(Component):
    template_name = "rating_badge/rating_badge.html"

    def get_context_data(self, rating=None, count=0, size="default"):
        """
        rating: float or None — the average score (e.g. 4.8)
        count:  int — total number of ratings
        size:   "default" | "large" — controls visual scale
        """
        # Build filled / half / empty star counts for a 5-star display
        stars = []
        if rating is not None:
            full = int(rating)
            has_half = (rating - full) >= 0.3
            stars = (
                ["full"] * full
                + (["half"] if has_half else [])
            )
            stars += ["empty"] * (5 - len(stars))
        return {
            "rating": rating,
            "count": count,
            "stars": stars,
            "size": size,
        }

    class Media:
        css = {"all": ["rating_badge/rating_badge.css"]}
