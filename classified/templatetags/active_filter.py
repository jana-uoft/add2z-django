from django import template
from classified.models import *

register = template.Library()

@register.filter
def active_filter(current_filter):
    result = []

    if not current_filter:
        return result

    for key,val in current_filter.items():
        if key == 'main_category':
            result.append(('main_category='+str(AdMainCategory.objects.get(id=val).id), AdMainCategory.objects.get(id=val)))
        elif key == 'sub_category':
            result.append(('sub_category='+str(AdSubCategory.objects.get(id=val).id), AdSubCategory.objects.get(id=val)))
        elif key == 'offer_price__gte':
            result.append((key+"="+val, "MIN: "+val+" $"))
        elif key == 'offer_price__lte':
            result.append((key+"="+val, "MAX: "+val+" $"))
        else:
            result.append((key+"="+val, val))

    return result
