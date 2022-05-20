import bleach
import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_markdown(value):
    return md.markdown(value, extensions=[
        'nl2br',
        'fenced_code',
        'codehilite',
        'pymdownx.inlinehilite',
        'pymdownx.tasklist',
        'pymdownx.mark',
        'pymdownx.keys',
        'pymdownx.magiclink',
        'pymdownx.tilde',
    ])


@register.filter
def limit_markdown(value):
    attrs = {
        'a': ['href', 'rel'],
        'img': ['alt', 'src', 'class'],
        'code': ['lang', 'class'],
        'pre': ['lang', 'class'],
        'span': ['class'],
        'ul': ['class'],
        'ol': ['class'],
        'li': ['class'],
        'input': ['type', 'vlue', 'disabled', 'checked'],
        'label': ['class'],
    }
    return bleach.clean(value, tags=[
        'input',
        'label',
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
        'a',
        'pre',
        'span',
        'mark',
        'kbd',
        's',
        'del',
    ], attributes=attrs, strip=True)
