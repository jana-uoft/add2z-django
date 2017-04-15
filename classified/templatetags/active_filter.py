from django import template
from classified.models import *
from django.utils import timezone


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
            result.append(("minPrice="+val, "MIN: "+val+" $"))
        elif key == 'offer_price__lte':
            result.append(("maxPrice="+val, "MAX: "+val+" $"))
        elif key == 'created_at__gte':
            days = (timezone.now()-val).days
            if days == 1:
                days = "1day"
            elif days == 7:
                days = "7days"
            elif days == 30:
                days = "30days"
            else:
                days = False
            if days:
                result.append(("posted_within="+days, days))
        else:
            result.append((key+"="+val, val))

    return result
