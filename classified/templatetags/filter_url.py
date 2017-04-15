from django import template
import copy
from django.utils import timezone



register = template.Library()

@register.filter
def filter_url(current_filter, new_filter=None):


    result = copy.deepcopy(current_filter)

    try:
        field = new_filter.split("=")[0]
        value = new_filter.split("=")[1]
    except:
        pass

    try:
        if field == 'main_category':
            del result['sub_category']
    except:
        pass

    try:
        if field == 'province':
            del result['city']
    except:
        pass

    # print result

    try:
        del result[field]
    except:
        pass

    try:
        result[field] = value
    except:
        pass

    try:
        if new_filter == 'remove_date':
            del result['created_at__gte']
    except:
        pass


    NEW_FILTER_STRING = ''
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'offer_price__gte', 'offer_price__lte', 'created_at__gte']:
        try:
            if key == 'created_at__gte':
                days = (timezone.now()-result['created_at__gte']).days
                if days == 1:
                    days = "1day"
                elif days == 7:
                    days = "7days"
                elif days == 30:
                    days = "30days"
                else:
                    days = "any"
                NEW_FILTER_STRING += "posted_within="+days+"&"
            elif key == 'offer_price__gte':
                value = str(result['offer_price__gte'])
                NEW_FILTER_STRING += "minPrice="+value+"&"
            elif key == 'offer_price__lte':
                value = str(result['offer_price__lte'])
                NEW_FILTER_STRING += "maxPrice="+value+"&"
            else:
                NEW_FILTER_STRING += key+"="+str(result[key])+"&"
        except:
            pass

    try:
        if NEW_FILTER_STRING[-1] == "&":
            return NEW_FILTER_STRING[:-1]
    except:
        pass

    # print NEW_FILTER_STRING
    return NEW_FILTER_STRING
