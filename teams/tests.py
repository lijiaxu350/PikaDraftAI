from django.test import TestCase
from django.urls import reverse
from .models import Team

class TeamBuilderTests(TestCase):

    # 1. Test teams home page loading
    def test_teams_home_page_status(self):
        response = self.client.get(reverse('teams_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams_home.html')

    # 2. Test creating a new team inserts default 6 empty slots into DB
    def test_team_creation_initializes_empty_slots(self):
        response = self.client.post(reverse('create_team'), {'team_name': 'My VGC Team'})
        self.assertEqual(response.status_code, 302) # Redirects to detail page
        
        team = Team.objects.first()
        self.assertIsNotNone(team)
        self.assertEqual(team.name, 'My VGC Team')
        self.assertEqual(len(team.slots), 6)
        self.assertEqual(team.slots[0]['pokemon_id'], None)

    # 3. Test updating slots Level, Nature, and EVs in DB
    def test_update_slot_settings(self):
        team = Team.objects.create(name='Pikachu Fans', slots=[
            {
                "pokemon_id": "25",
                "pokemon_name": "pikachu",
                "ev_hp": 0,
                "ev_attack": 0,
                "ev_defense": 0,
                "ev_sp_attack": 0,
                "ev_sp_defense": 0,
                "ev_speed": 0,
                "level": 50,
                "nature": "Hardy"
            }
        ])
        
        # Post new EV and level configurations
        response = self.client.post(reverse('slot_detail', args=[team.id, 0]), {
            'level': 100,
            'nature': 'Jolly',
            'ev_hp': 252,
            'ev_attack': 0,
            'ev_defense': 4,
            'ev_sp_attack': 0,
            'ev_sp_defense': 0,
            'ev_speed': 252
        })
        self.assertEqual(response.status_code, 302) # Redirects back to slot detail page
        
        team.refresh_from_db()
        self.assertEqual(team.slots[0]['level'], 100)
        self.assertEqual(team.slots[0]['nature'], 'Jolly')
        self.assertEqual(team.slots[0]['ev_hp'], 252)
        self.assertEqual(team.slots[0]['ev_speed'], 252)

    # 4. Test deleting a team removes it from the database
    def test_delete_team(self):
        team = Team.objects.create(name='To Be Deleted', slots=[])
        self.assertEqual(Team.objects.count(), 1)
        
        response = self.client.post(reverse('delete_team', args=[team.id]))
        self.assertEqual(response.status_code, 302) # Redirects to home list
        self.assertEqual(Team.objects.count(), 0)
