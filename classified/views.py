from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pypostalcode import PostalCodeDatabase
from django.shortcuts import redirect





TOP_OF_THE_PAGE_LISTINGS = Advertisement.objects.filter(approved=True, package__name="Top of The Page")
AD_CATEGORIES = {}
for sub_category in AdSubCategory.objects.all():
    if sub_category.parent_category in AD_CATEGORIES:
        AD_CATEGORIES[sub_category.parent_category] += [sub_category]
    else:
        AD_CATEGORIES[sub_category.parent_category] = [sub_category]


def index(request):
    context = { 'TOP_OF_THE_PAGE_LISTINGS': TOP_OF_THE_PAGE_LISTINGS,
                'AD_CATEGORIES': AD_CATEGORIES}
    return render(request, 'classified/home/home.html', context)


def listings(request, filters=None):
    filter_params = {}
    if filters:
        try:
            for param in filters.split("&"):
                if param.split("=")[0] == 'main_category':
                    filter_params[param.split("=")[0]] = AdMainCategory.objects.get(id=param.split("=")[1])
                elif param.split("=")[0] == 'sub_category':
                    filter_params[param.split("=")[0]] = AdSubCategory.objects.get(id=param.split("=")[1])
                elif param.split("=")[0] == 'minPrice':
                    filter_params['offer_price__gte'] = param.split("=")[1]
                elif param.split("=")[0] == 'maxPrice':
                    filter_params['offer_price__lte'] = param.split("=")[1]
                elif param.split("=")[0] == 'posted_within':
                    startDate = date.today()
                    if param.split("=")[1] == "1day":
                        startDate = startDate - timedelta(days=1)
                    elif param.split("=")[1] == "7days":
                        startDate = startDate - timedelta(days=7)
                    elif param.split("=")[1] == "30days":
                        startDate = startDate - timedelta(days=30)
                    if startDate != date.today() :
                        filter_params['created_at__gte'] = startdate
                else:
                    filter_params[param.split("=")[0]] = param.split("=")[1]
        except:
            pass

    page = request.GET.get('page', 1)
    ALL_ADS_AND_METAS = {}
    ADs = Advertisement.objects.exclude(package__name="Top of The Page").filter(approved=True, **filter_params)
    for ad in ADs:
        try:
            ALL_ADS_AND_METAS[ad] = AdvertisementMeta.objects.get(advertisement=ad).__dict__
            del ALL_ADS_AND_METAS[ad]['_state']
            del ALL_ADS_AND_METAS[ad]['id']
            del ALL_ADS_AND_METAS[ad]['advertisement_id']
        except:
            ALL_ADS_AND_METAS[ad] = {}

    paginator = Paginator(tuple(ALL_ADS_AND_METAS), 10)
    try:
        ALL_ADS_TUPLE = paginator.page(page)
    except PageNotAnInteger:
        ALL_ADS_TUPLE = paginator.page(1)
    except EmptyPage:
        ALL_ADS_TUPLE = paginator.page(paginator.num_pages)


    top_ads_count = Advertisement.objects.filter(approved=True, package__name="Top of The Page", **filter_params).count()
    top_ads_to_show = top_ads_count / paginator.num_pages
    ALL_TOP_ADS_AND_METAS = {}
    Ads = Advertisement.objects.filter(approved=True, package__name="Top of The Page", **filter_params)[:top_ads_to_show]
    for ad in Ads:
        try:
            ALL_TOP_ADS_AND_METAS[ad] = AdvertisementMeta.objects.get(advertisement=ad).__dict__
            del ALL_TOP_ADS_AND_METAS[ad]['_state']
            del ALL_TOP_ADS_AND_METAS[ad]['id']
            del ALL_TOP_ADS_AND_METAS[ad]['advertisement_id']
        except:
            ALL_TOP_ADS_AND_METAS[ad] = {}

    MAIN_CATEGORIES = AdMainCategory.objects.all()


    CURRENT_FILTERS = request.path.split("/")[3]
    NEW_FILTERS = {}
    SELECTED_MAIN_CATEGORY, SELECTED_SUB_CATEGORY, SELECTED_PROVINCE, SELECTED_CITY, SELECTED_OFFER_TYPE = (None,)*5
    MIN_PRICE, MAX_PRICE = "", ""
    main_cat_changed = False
    ONE_DAY_CHECKED = ""
    try:
        for f in CURRENT_FILTERS.split("&"):
            try:
                filter_field = f.split("=")[0]
                filter_value = f.split("=")[1]
                if filter_field == 'main_category':
                    SELECTED_MAIN_CATEGORY = AdMainCategory.objects.get(id=filter_value)
                    NEW_FILTERS['main_category='] = str(SELECTED_MAIN_CATEGORY.id)+'&'
                elif filter_field == 'sub_category':
                    try:
                        SELECTED_SUB_CATEGORY = AdSubCategory.objects.get(id=filter_value)
                        if SELECTED_SUB_CATEGORY.parent_category == SELECTED_MAIN_CATEGORY:
                            NEW_FILTERS['sub_category='] = str(SELECTED_SUB_CATEGORY.id)+'&'
                        else:
                            main_cat_changed = True
                    except:
                        continue
                elif filter_field == 'province':
                    SELECTED_PROVINCE = filter_value
                    NEW_FILTERS['province='] = filter_value+'&'
                elif filter_field == 'city':
                    SELECTED_CITY= filter_value
                    NEW_FILTERS['city='] = filter_value+'&'
                elif filter_field == 'offer_type':
                    SELECTED_OFFER_TYPE = filter_value
                    NEW_FILTERS['offer_type='] = filter_value+'&'
                elif filter_field == 'minPrice':
                    has_min_price = True
                    if filter_value != "0":
                        MIN_PRICE = filter_value
                        NEW_FILTERS['minPrice='] = filter_value+'&'
                elif filter_field == 'maxPrice':
                    has_max_price = True
                    if filter_value != "999999":
                        MAX_PRICE = filter_value
                        NEW_FILTERS['maxPrice='] = filter_value+'&'
                elif filter_field == 'posted_within':
                    if filter_value == "1day":
                        ONE_DAY_CHECKED = "checked"
                        # NEW_FILTERS['posted_within='] = filter_value+'&'

            except:
                continue
    except:
        pass

    print NEW_FILTERS
    NEW_FILTER_STRING = ''
    for key in ['main_category=', 'sub_category=', 'province=', 'city=', 'offer_type=', 'minPrice=', 'maxPrice=', 'posted_within=']:
        try:
            NEW_FILTER_STRING += key+NEW_FILTERS[key]
        except:
            continue

    NEW_FILTERS = NEW_FILTER_STRING
    print NEW_FILTERS

    print main_cat_changed
    if main_cat_changed:
        return redirect('classified:filter-listings', NEW_FILTERS)

    if SELECTED_MAIN_CATEGORY:
        SUB_CATEGORIES = AdSubCategory.objects.filter(parent_category=SELECTED_MAIN_CATEGORY)
    else:
        SUB_CATEGORIES = None


    pcdb = PostalCodeDatabase()
    ALL_LOCATIONS = {}
    for p in Advertisement.objects.order_by().values('postal_code').distinct():
        pc = p['postal_code'][:3].upper()
        location = pcdb[pc]
        try:
            ALL_LOCATIONS[location.province] += [location.city.split(" ")[0]]
        except:
            ALL_LOCATIONS[location.province] = [location.city.split(" ")[0]]

    return render(request, 'classified/listing/all_listings.html', {'ALL_ADS_AND_METAS': ALL_ADS_AND_METAS,
                                                                    'ALL_ADS_TUPLE': ALL_ADS_TUPLE, 
                                                                    'ALL_TOP_ADS_AND_METAS': ALL_TOP_ADS_AND_METAS,
                                                                    'MAIN_CATEGORIES': MAIN_CATEGORIES,
                                                                    'SUB_CATEGORIES': SUB_CATEGORIES,
                                                                    'SELECTED_MAIN_CATEGORY': SELECTED_MAIN_CATEGORY,
                                                                    'SELECTED_SUB_CATEGORY': SELECTED_SUB_CATEGORY,
                                                                    'NEW_FILTERS': NEW_FILTERS,
                                                                    'ALL_LOCATIONS': ALL_LOCATIONS,
                                                                    'SELECTED_PROVINCE': SELECTED_PROVINCE,
                                                                    'SELECTED_CITY': SELECTED_CITY,
                                                                    'SELECTED_OFFER_TYPE': SELECTED_OFFER_TYPE,
                                                                    'MIN_PRICE': MIN_PRICE,
                                                                    'MAX_PRICE': MAX_PRICE,})


def listing(request, listing_id):
    ad = Advertisement.objects.get(pk=listing_id)
    ALL_PHOTOS = ad.photos.split(",")
    try :
        META = AdvertisementMeta.objects.get(advertisement=ad).__dict__
        del META['_state']
        del META['id']
        del META['advertisement_id']
    except:
        META = None
    return render(request, 'classified/listing/single_listing.html', {'ad': ad,
                                                                'ALL_PHOTOS': ALL_PHOTOS,
                                                                'META': META})







def removeFilter(request, filters, remove):
    NEW_FILTERS = ''
    for f in filters.split("&"):
        try:
            if f == remove:
                continue
            else:
                NEW_FILTERS += f + '&'
        except:
            continue

    if NEW_FILTERS[-1] == "&":
        NEW_FILTERS = NEW_FILTERS[:-1]

    if not NEW_FILTERS:
        return redirect('classified:all-listings')

    return redirect('classified:filter-listings', NEW_FILTERS)




