from django.shortcuts import render
from django.http import HttpResponse
from .models import * 


TOP_OF_THE_PAGE_LISTINGS = Advertisement.objects.filter(approved=True, package__name="Top of The Page")
AD_CATEGORIES = {}
for sub_category in AdSubCategory.objects.all():
	if sub_category.parent_category in AD_CATEGORIES:
		AD_CATEGORIES[sub_category.parent_category] += [sub_category]
	else:
		AD_CATEGORIES[sub_category.parent_category] = [sub_category]


def index(request):
	context = {	'TOP_OF_THE_PAGE_LISTINGS': TOP_OF_THE_PAGE_LISTINGS,
				'AD_CATEGORIES': AD_CATEGORIES}
	return render(request, 'classified/home/home.html', context)


def listings(request):
	return render(request, 'classified/listings/listings.html', {})


def listing(request, listing_id):
	advertisement = Advertisement.objects.get(pk=listing_id)
	ALL_PHOTOS = advertisement.photos.split(",")
	try :
		META = AdvertisementMeta.objects.get(advertisement=advertisement).__dict__
		del META['_state']
		del META['id']
		del META['advertisement_id']
		print META
	except:
		META = None
	return render(request, 'classified/listing/listing.html', {'advertisement': advertisement,
																'ALL_PHOTOS': ALL_PHOTOS,
																'META': META})