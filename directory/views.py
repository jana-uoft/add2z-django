from django.shortcuts import render


# Create your views here.
def index(request):
	context = {"STATIC_URL": 'https://storage.googleapis.com/add2z/classifieds/'}
	return render(request, 'directory/coming_soon.html', context)