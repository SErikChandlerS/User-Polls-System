from django.contrib import admin

from main.models import Candidate, Vote


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["name", "votes"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["candidate", "ip_address"]
