from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.


class ZPTeamSnapShotListView(ListView):
    model = "ZPTeamSnapShot"
    template_name = "ZPTeamSnapShot_list.html"
