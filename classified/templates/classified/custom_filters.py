from django import template
register = template.Library()

@register.filter
def filter_url(current_filter, new_filter):
    new_filter_field = new_filter.split("=")[0]
    new_filter_value = new_filter.split("=")[1]

    NEW_FILTERS = ''
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
    return NEW_FILTERS
