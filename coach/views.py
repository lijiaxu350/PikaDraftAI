from django.shortcuts import render, get_object_or_404
from teams.models import Team
from .geminiAPI import Ask_AI
import json

# Create your views here.
def coach_home(request):
    teams = Team.objects.all()
    selected = None
    feedback = None
    
    team_id = request.GET.get("team_id")
    if team_id:
        selected = get_object_or_404(Team, id = team_id)
        team_json = json.dumps(selected.slots)
        try:
            feedback = Ask_AI(
                "You are a professional Pokemon VGC champion for 2v2 battles. " \
                "Here is my team, your job is to tell me what my strengths and weaknesses are, " \
                "what matchup archetypes I am good into and what matchup archetypes I am weak into. " \
                "Tell me some leading strategies I can open with. " \
                "You should refer to pikalytic.com for top 2v2 VGC teams. " \
                "Pay attention to the items being used on each pokemon. " \
                "Keep the response under 500 words.", team_json)
        except Exception as e:
            feedback = "Pikachu's brain is currently on high demand, please try again in a moment."
    return render(request, "coach.html", {
        "teams": teams,
        "selected_team": selected,
        "feedback": feedback,
        })