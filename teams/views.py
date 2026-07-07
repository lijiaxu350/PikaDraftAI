from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from pokedex.pokeapi import get_all_pokemon
from pokedex.pokeapi import get_pokemon


# Create your views here.

NATURES = {
    "Hardy":   {"boost": None, "lower": None},
    "Lonely":  {"boost": "attack", "lower": "defense"},
    "Brave":   {"boost": "attack", "lower": "speed"},
    "Adamant": {"boost": "attack", "lower": "special-attack"},
    "Naughty": {"boost": "attack", "lower": "special-defense"},
    "Bold":    {"boost": "defense", "lower": "attack"},
    "Docile":  {"boost": None, "lower": None},
    "Relaxed": {"boost": "defense", "lower": "speed"},
    "Impish":  {"boost": "defense", "lower": "special-attack"},
    "Lax":     {"boost": "defense", "lower": "special-defense"},
    "Timid":   {"boost": "speed", "lower": "attack"},
    "Hasty":   {"boost": "speed", "lower": "defense"},
    "Serious": {"boost": None, "lower": None},
    "Jolly":   {"boost": "speed", "lower": "special-attack"},
    "Naive":   {"boost": "speed", "lower": "special-defense"},
    "Modest":  {"boost": "special-attack", "lower": "attack"},
    "Mild":    {"boost": "special-attack", "lower": "defense"},
    "Quiet":   {"boost": "special-attack", "lower": "speed"},
    "Bashful": {"boost": None, "lower": None},
    "Rash":    {"boost": "special-attack", "lower": "special-defense"},
    "Calm":    {"boost": "special-defense", "lower": "attack"},
    "Gentle":  {"boost": "special-defense", "lower": "defense"},
    "Sassy":   {"boost": "special-defense", "lower": "speed"},
    "Careful": {"boost": "special-defense", "lower": "special-attack"},
    "Quirky":  {"boost": None, "lower": None},
}

ev_key_map = {
            "hp": "ev_hp",
            "attack": "ev_attack",
            "defense": "ev_defense",
            "special-attack": "ev_sp_attack",
            "special-defense": "ev_sp_defense",
            "speed": "ev_speed",
}
def calc_final_stats(pokemon, slot):
    level = slot.get("level", 100)
    nature_name = slot.get("nature", "Hardy")
    natures = NATURES[nature_name]

    final_stats = {}
    for stat in pokemon["stats"]:
        stat_name = stat["stat"]["name"]
        base = stat["base_stat"]
        ev = slot[ev_key_map[stat_name]]

        step1 = ((2 * base + 31 + (ev // 4)) * level) // 100
        if stat_name == "hp":
            final_stats[stat_name] = step1 + level + 10
        else:
            if stat_name == natures["boost"]:
                multiplier = 1.1
            elif stat_name == natures["lower"]:
                multiplier = 0.9
            else:
                multiplier = 1.0
            final_stats[stat_name] = int((step1 + 5) * multiplier)

    return final_stats

def create_team(request):
    if request.method == "POST":
        team_name = request.POST.get("team_name")

        empty_slots = []
        for _ in range(6):
            empty_slots.append({"pokemon_id": None,
                "pokemon_name": None,
                "ev_hp": 0,
                "ev_attack": 0, 
                "ev_defense": 0,
                "ev_sp_attack": 0, 
                "ev_sp_defense": 0, 
                "ev_speed": 0}
                )
        new_team = Team.objects.create(name=team_name, slots = empty_slots)
        return redirect("team_detail", team_id = new_team.id)
    
    return render(request, "create_team.html")

def teams_home(request):
    teams = Team.objects.all()
    return render(request, "teams_home.html", {"teams": teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id = team_id)
    return render(request, "team_detail.html", {"team": team})

def choose_pokemon(request, team_id, slot_index):
    team = get_object_or_404(Team, id=team_id)
    pokemon_all = get_all_pokemon()

    if request.method == "POST":
        pokemon_id = request.POST.get("pokemon_id")
        pokemon_name = request.POST.get("pokemon_name")

        team.slots[slot_index]["pokemon_id"] = pokemon_id
        team.slots[slot_index]["pokemon_name"] = pokemon_name
        team.save()

        return redirect("team_detail", team_id=team.id)
    
    for pokemon in pokemon_all:
        pokemon["id"] = pokemon["url"].rstrip("/").split("/")[-1]

    return render(request, "choose_pokemon.html", {"team": team, "pokemon_all": pokemon_all, "slot_index": slot_index})

def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        team.delete()
        return redirect("teams_home")

    return redirect("team_detail", team_id=team.id)

def slot_detail(request, team_id, slot_index):
    team = get_object_or_404(Team, id=team_id)
    slot = team.slots[slot_index]
    pokemon = get_pokemon(slot["pokemon_name"])

    if request.method == "POST":
        team.slots[slot_index]["ev_hp"] = int(request.POST.get("ev_hp", 0))
        team.slots[slot_index]["ev_attack"] = int(request.POST.get("ev_attack", 0))
        team.slots[slot_index]["ev_defense"] = int(request.POST.get("ev_defense", 0))
        team.slots[slot_index]["ev_sp_attack"] = int(request.POST.get("ev_sp_attack", 0))
        team.slots[slot_index]["ev_sp_defense"] = int(request.POST.get("ev_sp_defense", 0))
        team.slots[slot_index]["ev_speed"] = int(request.POST.get("ev_speed", 0))
        team.slots[slot_index]["level"] = int(request.POST.get("level", 100))
        team.slots[slot_index]["nature"] = request.POST.get("nature", "Hardy")
        team.slots[slot_index]["final_stats"] = calc_final_stats(pokemon, team.slots[slot_index])
        team.save()
        return redirect("slot_detail", team_id=team.id, slot_index=slot_index)

    level = slot.get("level", 100)
    nature_name = slot.get("nature", "Hardy")

    final_stats = calc_final_stats(pokemon, slot)

    return render(request, "slot_detail.html", {
        "team": team,
        "slot": slot,
        "slot_index": slot_index,
        "pokemon": pokemon,
        "final_stats": final_stats,
        "level": level,
        "nature_name": nature_name,
        "natures": NATURES.keys()
    })