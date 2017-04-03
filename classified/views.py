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
	return render(request, 'classified/home.html', context)


def listings(request):
	return render(request, 'classified/listings.html', {})


def listing(request, listing_id):
	if (listing_id=='1'):
		return render(request, 'classified/listing_other.html', {})
	elif (listing_id=='2'):
		return render(request, 'classified/listing_property.html', {})
	elif (listing_id=='3'):
		return render(request, 'classified/listing_auto.html', {})
	else:
		return render(request, 'classified/listing_job.html', {})