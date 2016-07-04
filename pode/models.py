from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class UserCodeManager(models.Manager):
    def create_from_title(self, owner, title, max_attempts=9999):
        base_slug = slugify(title)
        slug = base_slug
        i = 1

        while self.filter(owner=owner, slug=slug).exists():
            if i >= max_attempts:
                raise AssertionError('Maximum attempts reached!')
            i += 1
            slug = "%s-%d" % (base_slug, i)

        model = self.model(owner=owner, slug=slug)
        model.save()
        return model


class UserCode(models.Model):
    '''
    Represents a piece of code that a user has written.
    '''

    objects = UserCodeManager()

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

    def get_absolute_url(self):
        return reverse('pode:user_code', kwargs={
            'username': self.owner.username,
            'slug': self.slug
        })

    class Meta:
        verbose_name = 'User code asset'

        unique_together = (('owner', 'slug'),)
