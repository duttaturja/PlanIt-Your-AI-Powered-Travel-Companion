from django.shortcuts import render


def index(request):
    return render(request, "land.html")

def meet_the_devs(request):
    return render(request, "meet_the_devs.html")

def privacy_policy(request):
    return render(request, "privacy&policy.html")

def terms_of_services(request):
    return render(request, "terms&services.html")

def legal(request):
    return render(request, "legal.html")
