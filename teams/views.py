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

ITEMS = [#only going to include currently legal items in Pokemon Champions format
    "choice-band",
    "choice-scarf",
    "choice-specs",
    "life-orb",
    "focus-sash",
    "focus-band",
    "assault-vest",
    "eviolite",
    "rocky-helmet",
    "black-sludge",
    "heavy-duty-boots",
    "weakness-policy",
    "expert-belt",
    "light-clay",
    "quick-claw",
    "kings-rock",
    "scope-lens",
    "shell-bell",
    "white-herb",
    "mental-herb",
    "bright-powder",
    "black-belt",
    "black-glasses",
    "charcoal",
    "dragon-fang",
    "fairy-feather",
    "hard-stone",
    "magnet",
    "metal-coat",
    "miracle-seed",
    "mystic-water",
    "never-melt-ice",
    "poison-barb",
    "sharp-beak",
    "silk-scarf",
    "silver-powder",
    "soft-sand",
    "spell-tag",
    "twisted-spoon",
    "sitrus-berry",
    "oran-berry",
    "lum-berry",
    "leppa-berry",
    "cheri-berry",
    "chesto-berry",
    "pecha-berry",
    "rawst-berry",
    "persim-berry",
    "aspear-berry",
    "babiri-berry",
    "charti-berry",
    "chilan-berry",
    "chople-berry",
    "coba-berry",
    "colbur-berry",
    "haban-berry",
    "kasib-berry",
    "kebia-berry",
    "occa-berry",
    "passho-berry",
    "payapa-berry",
    "rindo-berry",
    "roseli-berry",
    "shuca-berry",
    "tanga-berry",
    "wacan-berry",
    "yache-berry",
    "abomasite",
    "absolite",
    "aerodactylite",
    "aggronite",
    "alakazite",
    "altarianite",
    "ampharosite",
    "audinite",
    "banettite",
    "barbaracite",
    "beedrillite",
    "blastoisinite",
    "blazikenite",
    "cameruptite",
    "chandelurite",
    "charizardite-x",
    "charizardite-y",
    "chesnaughtite",
    "chimechite",
    "clefablite",
    "crabominite",
    "delphoxite",
    "dragalgite",
    "dragoninite",
    "drampanite",
    "eelektrossite",
    "emboarite",
    "excadrite",
    "falinksite",
    "feraligite",
    "floettite",
    "froslassite",
    "galladite",
    "garchompite",
    "gardevoirite",
    "gengarite",
    "glalitite",
    "glimmoranite",
    "golurkite",
    "greninjite",
    "gyaradosite",
    "hawluchanite",
    "heracronite",
    "houndoominite",
    "kangaskhanite",
    "lopunnite",
    "lucarionite",
    "malamarite",
    "manectite",
    "mawilite",
    "medichamite",
    "meganiumite",
    "meowsticite",
    "metagrossite",
    "pidgeotite",
    "pinsirite",
    "pyroarite",
    "raichunite-x",
    "raichunite-y",
    "sablenite",
    "sceptilite",
    "scizorite",
    "scolipite",
    "scovillainite",
    "scraftinite",
    "sharpedonite",
    "skarmorite",
    "slowbronite",
    "staraptite",
    "starminite",
    "steelixite",
    "swampertite",
    "tyranitarite",
    "venusaurite",
    "victreebelite",
]

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

    ability_choices = [a["ability"]["name"] for a in pokemon["abilities"]]
    move_choices = sorted([m["move"]["name"] for m in pokemon["moves"]])

    if request.method == "POST":
        team.slots[slot_index]["ev_hp"] = int(request.POST.get("ev_hp", 0))
        team.slots[slot_index]["ev_attack"] = int(request.POST.get("ev_attack", 0))
        team.slots[slot_index]["ev_defense"] = int(request.POST.get("ev_defense", 0))
        team.slots[slot_index]["ev_sp_attack"] = int(request.POST.get("ev_sp_attack", 0))
        team.slots[slot_index]["ev_sp_defense"] = int(request.POST.get("ev_sp_defense", 0))
        team.slots[slot_index]["ev_speed"] = int(request.POST.get("ev_speed", 0))
        team.slots[slot_index]["level"] = int(request.POST.get("level", 100))
        team.slots[slot_index]["nature"] = request.POST.get("nature", "Hardy")
        

        submitted_ability = request.POST.get("ability", "")
        if submitted_ability in ability_choices:
            team.slots[slot_index]["ability"] = submitted_ability
        elif ability_choices:
            team.slots[slot_index]["ability"] = ability_choices[0]

        submitted_moves = []
        for i in range(1,5):
            move = request.POST.get(f"move_{i}", "")
            if move in move_choices:
                submitted_moves.append(move)
        team.slots[slot_index]["moves"] = submitted_moves

        submitted_item = request.POST.get("held_item", "")
        if submitted_item in ITEMS:
            team.slots[slot_index]["held_item"] = submitted_item
        else:
            team.slots[slot_index]["held_item"] = ""

        team.slots[slot_index]["final_stats"] = calc_final_stats(pokemon, team.slots[slot_index])
        team.save()
        return redirect("slot_detail", team_id=team.id, slot_index=slot_index)
    
    level = slot.get("level", 100)
    nature_name = slot.get("nature", "Hardy")
    ability_name = slot.get("ability", ability_choices[0] if ability_choices else "")
    current_moves = slot.get("moves", ["","","",""])
    while len(current_moves) < 4:
        current_moves.append("")

    held_item = slot.get("held_item", "")

    final_stats = calc_final_stats(pokemon, slot)

    return render(request, "slot_detail.html", {
        "team": team,
        "slot": slot,
        "slot_index": slot_index,
        "pokemon": pokemon,
        "final_stats": final_stats,
        "level": level,
        "nature_name": nature_name,
        "natures": NATURES.keys(),
        "abilities": ability_choices,
        "ability_name": ability_name,
        "moves": move_choices,
        "current_moves": current_moves,
        "items": ITEMS,
        "held_item": held_item,
    })

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teams_home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})