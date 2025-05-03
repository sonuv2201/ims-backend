from django.db import models, IntegrityError


class GenericBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra = models.JSONField(
        null=True, blank=True, default=dict, editable=False  # Default value for extra
    )

    def save(self, *args, **kwargs):
        max_retries = 100  # Maximum number of retries for ID conflicts
        for _ in range(max_retries):
            try:
                super().save(*args, **kwargs)  # Try saving the record
                break
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    # If there's a collision, manually set a new ID
                    self.id = (self.id or 0) + 1
                else:
                    raise  # Re-raise other exceptions
        else:
            raise IntegrityError("Unable to resolve ID conflict after retries.")

    class Meta:
        verbose_name = "Generic Base Model"
        verbose_name_plural = "Generic Base Models"

        abstract = True
