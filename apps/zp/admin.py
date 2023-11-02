from django.contrib import admin
from .models import TeamRiders, TeamPending, TeamResults, Profile, ProfileVictims, ProfileSignups

# Register your models here.
@admin.register(TeamRiders)
class TeamRidersAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(TeamPending)
class TeamPendingAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(TeamResults)
class TeamResultsAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(ProfileVictims)
class ProfileVictimsAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

@admin.register(ProfileSignups)
class ProfileSignupsAdmin(admin.ModelAdmin):
    list_display = ['modified_at', 'created_at']

