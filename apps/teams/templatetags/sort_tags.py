from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_url(context, field):
    request = context['request']
    current_sort = request.GET.get('sort', '')
    new_sort = field if current_sort != field else f'-{field}' if not current_sort.startswith(
        '-') else field.strip('-')
    return f'?sort={new_sort}'
