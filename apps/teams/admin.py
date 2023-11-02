from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'zp_id', 'zw_id', 'modified_at', 'created_at']
    search_fields = ['team_name', 'zp_id', 'zw_id']
    list_filter = ['modified_at', 'created_at']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'is_owner', 'is_admin', 'modified_at', 'created_at']
    search_fields = ['user__username', 'status']
    list_filter = ['status', 'is_owner', 'is_admin', 'modified_at', 'created_at']

