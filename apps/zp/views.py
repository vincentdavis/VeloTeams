from django.views.generic import ListView


class ZPTeamSnapShotListView(ListView):
    model = "ZPTeamSnapShot"
    template_name = "ZPTeamSnapShot_list.html"
