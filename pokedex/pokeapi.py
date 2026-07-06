import requests

pokemon_cache = {}

POKEAPI_URL = "https://pokeapi.co/api/v2"

def get_pokemon(nameID):

    key = str(nameID).lower()

    if key in pokemon_cache:
        return pokemon_cache[key]

    response = requests.get(f"{POKEAPI_URL}/pokemon/{key}")

    if response.status_code != 200:
        return None

    data = response.json()
    
    pokemon_cache[key] = data

    return data

pokemon_list_cache = None 

def get_all_pokemon():
    global pokemon_list_cache

    if pokemon_list_cache is not None:
        return pokemon_list_cache
    
    response = requests.get(f"{POKEAPI_URL}/pokemon?limit=2000")

    if response.status_code != 200:
        return None
    data = response.json()
    pokemon_list_cache = data["results"]

    return pokemon_list_cache