from django.test import TestCase
from .pokeapi import get_pokemon
from unittest.mock import patch
# Create your tests here.

class GetPokemonTest(TestCase):
    @patch("pokedex.pokeapi.requests.get")
    def test_get_pokemon_returns_correct_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 25,
            "name": "pikachu",
            "stats": [
                {"stat": {"name": "hp"}, "base_stat": 35},
                {"stat": {"name": "attack"}, "base_stat": 55},
            ],
        }

        pokemon = get_pokemon("pikachu")

        self.assertEqual(pokemon["name"], "pikachu")
        self.assertEqual(pokemon["id"], 25)