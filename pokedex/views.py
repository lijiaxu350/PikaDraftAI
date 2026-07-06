from django.shortcuts import render
from pokedex.pokeapi import get_all_pokemon
# Create your views here.

def pokedex_list(request):
    raw_list = get_all_pokemon()

    pokemon_list = []
    
    for pokemon in raw_list:
        pokemon_id = pokemon["url"].rstrip("/").split("/")[-1]
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"

        pokemon_list.append({
            "name": pokemon["name"],
            "id": pokemon_id,
            "sprite_url": sprite_url,
        })

    return render(request, 'pokedex.html', {'pokemon_list': pokemon_list})