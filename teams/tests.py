from django.test import TestCase
from django.urls import reverse
from .models import Team

class TeamBuilderTests(TestCase):

    # test teams home page loading
    def test_teams_home_page_status(self):
        response = self.client.get(reverse('teams_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams_home.html')

    #  test creating a new team inserts default 6 empty slots into DB
    def test_team_creation_initializes_empty_slots(self):
        response = self.client.post(reverse('create_team'), {'team_name': 'My VGC Team'})
        self.assertEqual(response.status_code, 302) # should go to details page
        
        team = Team.objects.first()
        self.assertIsNotNone(team)
        self.assertEqual(team.name, 'My VGC Team')
        self.assertEqual(len(team.slots), 6)
        self.assertEqual(team.slots[0]['pokemon_id'], None)
