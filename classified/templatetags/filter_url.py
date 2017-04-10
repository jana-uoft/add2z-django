from django import template
register = template.Library()

@register.filter
def filter_url(current_filter, new_filter):
    new_filter_field = new_filter.split("=")[0]
    new_filter_value = new_filter.split("=")[1]

    NEW_FILTERS = ''
    if not current_filter:
        return new_filter

    for f in current_filter.split("&"):
        try:
            filter_field = f.split("=")[0]
            filter_value = f.split("=")[1]
            if filter_field == new_filter_field:
                NEW_FILTERS += new_filter+'&'
            else:
                NEW_FILTERS += f+'&'
        except:
            continue

    if new_filter not in NEW_FILTERS:
        NEW_FILTERS += new_filter+'&'

    if NEW_FILTERS[-1] == "&":
        return NEW_FILTERS[:-1]
    return NEW_FILTERS
