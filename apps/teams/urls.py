from django.urls import path
from .views import TeamCreateView, TeamUpdateView, TeamListView, JoinTeamView, TeamAdminView, JoinTeamIDView, TeamProfileView, TeamListViewCreate
app_name = "teams"
urlpatterns = [
    path('team/create/', TeamCreateView.as_view(), name='team_create'),
    path('team/update/<int:pk>/', TeamUpdateView.as_view(), name='team_update'),
    path('teams/', TeamListViewCreate.as_view(), name='team_list'),
    # path('team/join/', JoinTeamView.as_view(), name='team_join'),
    path('team/join/<int:team_id>/', JoinTeamIDView.as_view(), name='team_join_id'),
    path('team/admin/<int:team_id>/', TeamAdminView.as_view(), name='team_admin'),
    path('team/<int:pk>/', TeamProfileView.as_view(), name='team_profile'),
]
