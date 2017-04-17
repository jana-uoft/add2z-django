from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pypostalcode import PostalCodeDatabase
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *


try:
    user_profile = UserProfile.objects.get(user=request.user)
except:
    user_profile = ""

AD_CATEGORIES = {}
for sub_category in AdSubCategory.objects.all():
    if sub_category.parent_category in AD_CATEGORIES:
        AD_CATEGORIES[sub_category.parent_category] += [sub_category]
    else:
        AD_CATEGORIES[sub_category.parent_category] = [sub_category]
pcdb = PostalCodeDatabase()
ALL_LOCATIONS = {}
for p in Advertisement.objects.order_by().values('postal_code').distinct():
    pc = p['postal_code'][:3].upper()
    location = pcdb[pc]
    try:
        ALL_LOCATIONS[location.province] += [location.city.split(" ")[0]]
    except:
        ALL_LOCATIONS[location.province] = [location.city.split(" ")[0]]



def index(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = ""
    TOP_OF_THE_PAGE_LISTINGS = Advertisement.objects.filter(approved=True, package__name="Top of The Page")

    context = { 'TOP_OF_THE_PAGE_LISTINGS': TOP_OF_THE_PAGE_LISTINGS,
                'AD_CATEGORIES': AD_CATEGORIES,
                'ALL_LOCATIONS': ALL_LOCATIONS,
                'user_profile': user_profile}

    return render(request, 'classified/home/home.html', context)


def listings(request, filters=None):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = ""
    CURRENT_FILTERS = {}
    SELECTED_MAIN_CATEGORY, SELECTED_SUB_CATEGORY, SELECTED_PROVINCE, SELECTED_CITY, SELECTED_OFFER_TYPE = ("",)*5
    MIN_PRICE, MAX_PRICE = "", ""
    ONE_DAY_CHECKED, SEVEN_DAY_CHECKED, ONE_MONTH_CHECKED, ANY_DAY_CHECKED = ("",)*4
    SEARCH_PARAM = ""
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
                    startDate = timezone.now()
                    if value == "1day":
                        startDate = startDate - timedelta(days=1)
                        ONE_DAY_CHECKED = "checked"
                    elif value == "7days":
                        startDate = startDate - timedelta(days=7)
                        SEVEN_DAY_CHECKED = "checked"
                    elif value == "30days":
                        startDate = startDate - timedelta(days=30)
                        ONE_MONTH_CHECKED = "checked"
                    if startDate.day != timezone.now().day :
                        CURRENT_FILTERS['created_at__gte'] = startDate
                    else:
                        ANY_DAY_CHECKED = "checked"
                elif field == 'title__icontains':
                    SEARCH_PARAM = value
                else:
                    CURRENT_FILTERS[field] = value
        except:
            pass

    pcdb = PostalCodeDatabase()
    ALL_LOCATIONS = {}
    for p in Advertisement.objects.order_by().values('postal_code').distinct():
        pc = p['postal_code'][:3].upper()
        location = pcdb[pc]
        try:
            ALL_LOCATIONS[location.province] += [location.city.split(" ")[0]]
        except:
            ALL_LOCATIONS[location.province] = [location.city.split(" ")[0]]


    if not ONE_DAY_CHECKED and not SEVEN_DAY_CHECKED and not ONE_MONTH_CHECKED:
        ANY_DAY_CHECKED = "checked"

    if not SELECTED_MAIN_CATEGORY:
        try:
            SELECTED_MAIN_CATEGORY = AdSubCategory.objects.get(id=SELECTED_SUB_CATEGORY).parent_category.id
        except:
            pass

    if not SELECTED_PROVINCE and SELECTED_CITY:
        try:
            SELECTED_PROVINCE = ""
            for province, cities in ALL_LOCATIONS.items():
                if SELECTED_CITY in cities:
                    SELECTED_PROVINCE = province
                    break
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





    if SELECTED_CITY:
        if SELECTED_CITY not in ALL_LOCATIONS[SELECTED_PROVINCE]:
            del CURRENT_FILTERS['city']
            SELECTED_CITY = None

    

    NEW_FILTER_STRING = ''
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'offer_price__gte', 'offer_price__lte', 'created_at__gte']:
        try:
            if key == 'created_at__gte':
                days = (timezone.now()-CURRENT_FILTERS[key]).days
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
                value = str(CURRENT_FILTERS[key])
                NEW_FILTER_STRING += "minPrice="+value+"&"
            elif key == 'offer_price__lte':
                value = str(CURRENT_FILTERS[key])
                NEW_FILTER_STRING += "maxPrice="+value+"&"
            else:
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
                                                                    'NEW_FILTER_STRING': NEW_FILTER_STRING,
                                                                    'ONE_DAY_CHECKED': ONE_DAY_CHECKED,
                                                                    'SEVEN_DAY_CHECKED': SEVEN_DAY_CHECKED,
                                                                    'ONE_MONTH_CHECKED': ONE_MONTH_CHECKED,
                                                                    'ANY_DAY_CHECKED': ANY_DAY_CHECKED,
                                                                    'AD_CATEGORIES': AD_CATEGORIES,
                                                                    'ALL_LOCATIONS': ALL_LOCATIONS,
                                                                    'SEARCH_PARAM': SEARCH_PARAM,
                                                                    'user_profile': user_profile})






def listing(request, listing_id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = ""
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
                                                                'META': META,
                                                                'AD_CATEGORIES': AD_CATEGORIES,
                                                                'ALL_LOCATIONS': ALL_LOCATIONS,
                                                                'user_profile': user_profile})







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
    for key in ['main_category', 'sub_category', 'province', 'city', 'offer_type', 'minPrice', 'maxPrice', 'posted_within']:
        try:
            if key == 'posted_within':
                days = (timezone.now()-NEW_FILTERS[key]).days
                if days == 1:
                    days = "1day"
                elif days == 7:
                    days = "7days"
                elif days == 30:
                    days = "30days"
                else:
                    days = "any"
                NEW_FILTER_STRING += "posted_within="+days+"&"
            else:
                NEW_FILTER_STRING += key+"="+str(NEW_FILTERS[key])+"&"
        except:
            continue


    if not NEW_FILTER_STRING:
        return redirect('classified:all-listings')

    if NEW_FILTER_STRING[-1] == "&":
        NEW_FILTER_STRING = NEW_FILTER_STRING[:-1]

    return redirect('classified:filter-listings', NEW_FILTER_STRING)









@login_required(login_url="/classifieds/accounts/login/", redirect_field_name=None)
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = ""
    return render(request, 'classified/account/profile_home.html', {'user_profile': user_profile,
                                                                    'AD_CATEGORIES': AD_CATEGORIES,
                                                                    'ALL_LOCATIONS': ALL_LOCATIONS,})




def sign_in(request):
    pass


def sign_out(request):
    pass


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('classified:profile')

    return render(request, 'classified/account/register.html', {'form': form})