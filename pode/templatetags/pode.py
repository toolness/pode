from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def code_share_url(context, code):
    return code.get_absolute_url_for_sharing(context['request'])
