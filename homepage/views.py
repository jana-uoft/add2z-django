from django.shortcuts import render


context = {"STATIC_URL" : "https://storage.googleapis.com/add2z/homepage/"}



def index(request):
	return render(request, 'homepage/index.html', context)