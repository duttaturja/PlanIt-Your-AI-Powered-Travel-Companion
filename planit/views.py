from django.shortcuts import render


def index(request):
    return render(request, "land.html")

def meet_the_devs(request):
    return render(request, "meet_the_devs.html")
