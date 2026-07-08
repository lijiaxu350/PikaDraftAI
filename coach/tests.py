from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from teams.models import Team
import json
# Create your tests here.

class GeminiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.team = Team.objects.create(
            name="Test Squad",
            slots=[
                {
                    "pokemon_id": "25",
                    "pokemon_name": "pikachu",
                    "ev_hp": 2,
                    "ev_attack": 32,
                    "ev_defense": 0,
                    "ev_sp_attack": 0,
                    "ev_sp_defense": 0,
                    "ev_speed": 32,
                    "level": 100,
                    "nature": "Jolly",
                    "ability": "static",
                    "moves": ["thunderbolt", "volt-tackle", "iron-tail", ""],
                    "held_item": "light-ball",
                },
            ],
        )

    def test_gemini_receives_correct_team_json(self):
        with patch("coach.views.Ask_AI") as mock_ask_ai:
            mock_ask_ai.return_value = "mocked feedback"

            self.client.get(reverse("coach_home"),{"team_id":self.team.id})

        prompt_arg, team_json_arg = mock_ask_ai.call_args[0]

        parsed = json.loads(team_json_arg)
        self.assertEqual(parsed, self.team.slots)

        self.assertEqual(parsed[0]["pokemon_name"], "pikachu")
        self.assertEqual(parsed[0]["held_item"], "light-ball")
        self.assertIn("thunderbolt", parsed[0]["moves"])