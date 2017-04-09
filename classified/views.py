from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
        for param in filters.split("&"):
            filter_params[param.split("=")[0]] = param.split("=")[1]
            print filter_params

    page = request.GET.get('page', 1)
    ALL_ADS_AND_METAS = {}
    for ad in Advertisement.objects.exclude(package__name="Top of The Page").filter(approved=True, **filter_params):
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
    for ad in Advertisement.objects.filter(approved=True, package__name="Top of The Page", **filter_params)[:top_ads_to_show]:
        try:
            ALL_TOP_ADS_AND_METAS[ad] = AdvertisementMeta.objects.get(advertisement=ad).__dict__
            del ALL_TOP_ADS_AND_METAS[ad]['_state']
            del ALL_TOP_ADS_AND_METAS[ad]['id']
            del ALL_TOP_ADS_AND_METAS[ad]['advertisement_id']
        except:
            ALL_TOP_ADS_AND_METAS[ad] = {}
    print ALL_TOP_ADS_AND_METAS

    return render(request, 'classified/listing/all_listings.html', {'ALL_ADS_AND_METAS': ALL_ADS_AND_METAS,
                                                                    'ALL_ADS_TUPLE': ALL_ADS_TUPLE, 
                                                                    'ALL_TOP_ADS_AND_METAS': ALL_TOP_ADS_AND_METAS})


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