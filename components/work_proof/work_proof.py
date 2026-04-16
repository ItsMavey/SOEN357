from django_components import Component, register


@register("work_proof")
class WorkProof(Component):
    template_name = "work_proof/work_proof.html"

    def get_context_data(self, proof):
        """
        proof: a WorkProof model instance with photo_before, photo_after,
               caption, worker, and created_at.
        """
        exif_before = proof.exif_entries.filter(
            image_field_name="photo_before"
        ).first()
        exif_after = proof.exif_entries.filter(
            image_field_name="photo_after"
        ).first()
        return {
            "proof": proof,
            "exif_before": exif_before,
            "exif_after": exif_after,
        }

    class Media:
        css = {"all": ["work_proof/work_proof.css"]}
