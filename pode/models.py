from django.db import models
from django.contrib.auth.models import User


class UserCode(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    slug = models.SlugField(
        help_text='Slug for the content.',
        blank=False,
        null=False
    )

    content = models.TextField(
        help_text='Raw HTML code.'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return '%s/%s' % (self.owner.username, self.slug)
