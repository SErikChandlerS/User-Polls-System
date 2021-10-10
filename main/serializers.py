from rest_framework import serializers
from main.models import Candidate, Vote
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class CandidateSerializer(serializers.ModelSerializer):
    votes = serializers.ReadOnlyField()

    class Meta:
        model = Candidate
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField()

    def create(self, validated_data):
        candidate = get_object_or_404(Candidate, name=validated_data["candidate_name"])
        vote = Vote()
        vote.candidate = candidate
        try:
            vote.save(commit=False)
        except IntegrityError:
            return vote
        return vote

    class Meta:
        model = Vote
        exclude = ("id", "ip_address", "candidate")
