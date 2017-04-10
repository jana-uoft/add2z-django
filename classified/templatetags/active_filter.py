from django import template
from classified.models import *

register = template.Library()

@register.filter
def active_filter(current_filter):

    result = {}

    # print current_filter
    if not current_filter:
        return result

    for f in current_filter.split("&"):
        try:
            filter_field = f.split("=")[0]
            filter_value = f.split("=")[1]
            if filter_field == 'main_category':
                SELECTED_MAIN_CATEGORY = AdMainCategory.objects.get(id=filter_value)
                result[SELECTED_MAIN_CATEGORY.name] = 'main_category='+filter_value
            elif filter_field == 'sub_category':
                SELECTED_SUB_CATEGORY = AdSubCategory.objects.get(id=filter_value)
                result[SELECTED_SUB_CATEGORY.name] = 'sub_category='+filter_value
            else:
                result[filter_value] = f
        except:
            continue

    # print result

    return result
