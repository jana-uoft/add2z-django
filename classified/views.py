from django.shortcuts import render
from django.http import HttpResponse


context = {"STATIC_URL" : "https://storage.googleapis.com/add2z/classifieds/"}


def index(request):
	return render(request, 'classified/home.html', context)


def listings(request):
	return render(request, 'classified/listings.html', context)


def listing(request, listing_id):
	if (listing_id=='1'):
		return render(request, 'classified/listing_other.html', context)
	elif (listing_id=='2'):
		return render(request, 'classified/listing_property.html', context)
	elif (listing_id=='3'):
		return render(request, 'classified/listing_auto.html', context)
	else:
		return render(request, 'classified/listing_job.html', context)