from django import template
import copy



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

    try:
        del result[field]
    except:
        pass

    try:
        result[field] = value
    except:
        pass

    NEW_FILTER_STRING = ''
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'minPrice', 'maxPrice', 'posted_within']:
        try:
            NEW_FILTER_STRING += key+"="+str(result[key])+"&"
        except:
            pass

    try:
        if NEW_FILTER_STRING[-1] == "&":
            return NEW_FILTER_STRING[:-1]
    except:
        pass

    return NEW_FILTER_STRING
