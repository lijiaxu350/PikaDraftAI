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
                "You are a professional Pokemon VGC champion for 2v2 battles, the current set is Pokemon Champions M-4. " \
                "Here is my team, your job is to tell me:" \
                "1. What my strengths and weaknesses are, " \
                "2. What matchup archetypes I am good into and what matchup archetypes I am weak into. (EX: Rain Teams, Sun Teams, Snow Teams, Trick Room, Tailwind, Etc.)" \
                "3. Tell me some leading strategies I can open with (EX: Most of the time use these two pokemon, edge cases to use something else). " \
                "4. You should refer to pikalytic.com for top 2v2 Pokemon Champions VGC teams. " \
                "5. Pay attention to the HELD ITEMS, MOVES, NATURES, and ABILITIES the pokemons have. " \
                "7. Give advice on who to BENCH unless for a specific pokemon or matchup." \
                "8. IMPORTANT: MAKE SURE YOU ARE GIVING RESPONSES BASED ON POKEMONS IN THE POKEMON CHAMPIONS FORMAT, NOT GENERAL VGC. IF THE GIVEN TEAM HAS POKEMON OUTSIDE THE FORMAT" \
                "GIVE A RESPONSE, BUT NOTE THAT THAT SPECIFIC POKEMON IS OUTSIDE THE FORMAT AND TRY TO SUB IN A POKEMON IN THE FORMAT."
                "9. Keep the response under 500 words.", team_json)
        except Exception as e:
            feedback = "Pikachu's brain is currently on high demand, please try again in a moment."
    return render(request, "coach.html", {
        "teams": teams,
        "selected_team": selected,
        "feedback": feedback,
        })