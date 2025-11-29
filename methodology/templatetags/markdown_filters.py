"""
Django template filters for Markdown rendering.
"""

from django import template
from django.utils.safestring import mark_safe
from methodology.utils.markdown_renderer import render_markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value):
    """
    Convert Markdown text to safe HTML.
    
    Usage in templates:
        {{ activity.guidance|markdown }}
    
    :param value: Markdown text string
    :return: Safe HTML string marked as safe for Django templates
    """
    if not value:
        return ''
    
    html = render_markdown(value)
    return mark_safe(html)
