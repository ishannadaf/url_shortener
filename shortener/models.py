from django.db import models
from .utils import encode_base62


class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.short_code = encode_base62(self.id)
            super().save(update_fields=['short_code'])

    def __str__(self):
        return self.short_code