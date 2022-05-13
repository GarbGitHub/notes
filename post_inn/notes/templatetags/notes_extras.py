import bleach
import markdown
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_markdown(value):
    return markdown.markdown(value, extensions=[
        'markdown.extensions.fenced_code', 'nl2br',
        'fenced_code',
        'sane_lists'
    ])


@register.filter
def limit_markdown(value):
    attrs = {
        'a': ['href', 'rel'],
        'img': ['alt', 'src', 'class'],
    }
    return bleach.clean(value, tags=[
        'br',
        'strong',
        'p',
        'i',
        'em',
        'img',
        'ol',
        'ul',
        'li',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'blockquote',
        'code',
        'a'
    ], attributes=attrs, strip=True)
