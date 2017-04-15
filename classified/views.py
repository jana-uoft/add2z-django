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
    CURRENT_FILTERS = {}
    SELECTED_MAIN_CATEGORY, SELECTED_SUB_CATEGORY, SELECTED_PROVINCE, SELECTED_CITY, SELECTED_OFFER_TYPE = (None,)*5
    MIN_PRICE, MAX_PRICE = "", ""
    ONE_DAY_CHECKED, SEVEN_DAY_CHECKED, ONE_MONTH_CHECKED, ANY_DAY_CHECKED = (None,)*4
    if filters:
        try:
            for param in filters.split("&"):
                field = param.split("=")[0]
                value = param.split("=")[1]
                if field == 'main_category':
                    CURRENT_FILTERS[field] = AdMainCategory.objects.get(id=value).id
                    SELECTED_MAIN_CATEGORY = CURRENT_FILTERS[field]
                elif field == 'sub_category':
                    CURRENT_FILTERS[field] = AdSubCategory.objects.get(id=value).id
                    SELECTED_SUB_CATEGORY = CURRENT_FILTERS[field]
                elif field == 'province':
                    CURRENT_FILTERS[field] = value
                    SELECTED_PROVINCE = value
                elif field == 'city':
                    CURRENT_FILTERS[field] = value
                    SELECTED_CITY = value
                elif field == 'minPrice':
                    CURRENT_FILTERS['offer_price__gte'] = value
                    MIN_PRICE = value
                elif field == 'maxPrice':
                    CURRENT_FILTERS['offer_price__lte'] = value
                    MAX_PRICE = value
                elif field == 'posted_within':
                    startDate = date.today()
                    if value == "1day":
                        startDate = startDate - timedelta(days=1)
                    elif value == "7days":
                        startDate = startDate - timedelta(days=7)
                    elif value == "30days":
                        startDate = startDate - timedelta(days=30)
                    if startDate != date.today() :
                        CURRENT_FILTERS['created_at__gte'] = startdate
                else:
                    CURRENT_FILTERS[field] = value
        except:
            pass


    if not SELECTED_MAIN_CATEGORY:
        try:
            del CURRENT_FILTERS['sub_category']
            SELECTED_SUB_CATEGORY = None
        except:
            pass

    if not SELECTED_PROVINCE:
        try:
            del CURRENT_FILTERS['city']
            SELECTED_CITY = None
        except:
            pass


    page = request.GET.get('page', 1)
    ALL_ADS_AND_METAS = {}
    ADs = Advertisement.objects.exclude(package__name="Top of The Page").filter(approved=True, **CURRENT_FILTERS)
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


    top_ads_count = Advertisement.objects.filter(approved=True, package__name="Top of The Page", **CURRENT_FILTERS).count()
    top_ads_to_show = top_ads_count / paginator.num_pages
    ALL_TOP_ADS_AND_METAS = {}
    Ads = Advertisement.objects.filter(approved=True, package__name="Top of The Page", **CURRENT_FILTERS)[:top_ads_to_show]
    for ad in Ads:
        try:
            ALL_TOP_ADS_AND_METAS[ad] = AdvertisementMeta.objects.get(advertisement=ad).__dict__
            del ALL_TOP_ADS_AND_METAS[ad]['_state']
            del ALL_TOP_ADS_AND_METAS[ad]['id']
            del ALL_TOP_ADS_AND_METAS[ad]['advertisement_id']
        except:
            ALL_TOP_ADS_AND_METAS[ad] = {}

    MAIN_CATEGORIES = AdMainCategory.objects.all()


    if SELECTED_MAIN_CATEGORY:
        SUB_CATEGORIES = AdSubCategory.objects.filter(parent_category=SELECTED_MAIN_CATEGORY)
    else:
        SUB_CATEGORIES = None
    

    if SELECTED_SUB_CATEGORY:
        if AdSubCategory.objects.get(id=SELECTED_SUB_CATEGORY).parent_category.id != SELECTED_MAIN_CATEGORY:
            del CURRENT_FILTERS['sub_category']
            SELECTED_SUB_CATEGORY = None


    pcdb = PostalCodeDatabase()
    ALL_LOCATIONS = {}
    for p in Advertisement.objects.order_by().values('postal_code').distinct():
        pc = p['postal_code'][:3].upper()
        location = pcdb[pc]
        try:
            ALL_LOCATIONS[location.province] += [location.city.split(" ")[0]]
        except:
            ALL_LOCATIONS[location.province] = [location.city.split(" ")[0]]


    if SELECTED_CITY:
        if SELECTED_CITY not in ALL_LOCATIONS[SELECTED_PROVINCE]:
            del CURRENT_FILTERS['city']
            SELECTED_CITY = None


    NEW_FILTER_STRING = ''
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'offer_price__gte', 'offer_price__lte', 'posted_within']:
        try:
            NEW_FILTER_STRING += key+"="+str(CURRENT_FILTERS[key])+"&"
        except:
            continue


    return render(request, 'classified/listing/all_listings.html', {'ALL_ADS_AND_METAS': ALL_ADS_AND_METAS,
                                                                    'ALL_ADS_TUPLE': ALL_ADS_TUPLE, 
                                                                    'ALL_TOP_ADS_AND_METAS': ALL_TOP_ADS_AND_METAS,
                                                                    'MAIN_CATEGORIES': MAIN_CATEGORIES,
                                                                    'SUB_CATEGORIES': SUB_CATEGORIES,
                                                                    'SELECTED_MAIN_CATEGORY': SELECTED_MAIN_CATEGORY,
                                                                    'SELECTED_SUB_CATEGORY': SELECTED_SUB_CATEGORY,
                                                                    'ALL_LOCATIONS': ALL_LOCATIONS,
                                                                    'SELECTED_PROVINCE': SELECTED_PROVINCE,
                                                                    'SELECTED_CITY': SELECTED_CITY,
                                                                    'SELECTED_OFFER_TYPE': SELECTED_OFFER_TYPE,
                                                                    'MIN_PRICE': MIN_PRICE,
                                                                    'MAX_PRICE': MAX_PRICE,
                                                                    'CURRENT_FILTERS': CURRENT_FILTERS,
                                                                    'NEW_FILTER_STRING': NEW_FILTER_STRING})






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
    NEW_FILTERS = {}
    for f in filters.split("&"):
        try:
            if f == remove:
                continue
            else:
                field = f.split("=")[0]
                value = f.split("=")[1]
                NEW_FILTERS[field] = value
        except:
            continue

    try:
        NEW_FILTERS['main_category']
    except:
        try:
            del NEW_FILTERS['sub_category']
        except:
            pass

    try:
        NEW_FILTERS['province']
    except:
        try:
            del NEW_FILTERS['city']
        except:
            pass


    NEW_FILTER_STRING = ''
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'offer_price__gte', 'offer_price__lte', 'posted_within']:
        try:
            NEW_FILTER_STRING += key+"="+str(NEW_FILTERS[key])+"&"
        except:
            continue


    if not NEW_FILTER_STRING:
        return redirect('classified:all-listings')

    if NEW_FILTER_STRING[-1] == "&":
        NEW_FILTER_STRING = NEW_FILTER_STRING[:-1]

    return redirect('classified:filter-listings', NEW_FILTER_STRING)




