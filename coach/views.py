from django.shortcuts import render

# Create your views here.
def coach_home(request):
    return render(request, "coach.html")