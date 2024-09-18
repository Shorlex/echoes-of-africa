from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Hero, Comment

class HeroCreationTest(TestCase):
    def setUp(self):
        # Create a user to authenticate with
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_hero_creation_requires_login(self):
        # Try to access the hero creation page without logging in
        response = self.client.get(reverse('post_hero'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_hero_creation_with_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')

        # Make a POST request to create a hero
        response = self.client.post(reverse('post_hero'), {
            'name': 'Test Hero',
            'nationality': 'Test Nationality',
            'year_of_birth': '2000',
            'year_of_death': '2024',
            'body': 'A hero description',
        })
        # Assert the response is a redirect after successful creation
        self.assertEqual(response.status_code, 302)
        # print(response.context['form'].errors)
        # Optionally, you can check if the hero was created
        self.assertTrue(Hero.objects.filter(name='Test Hero').exists())

    def test_hero_creation_form_validation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post_hero'), {
            'name': '',  # Name is required, so this should trigger an error
            'description': 'Test without a name',
            'year_of_birth': '1980',
        }, follow=True)

        self.assertEqual(response.status_code, 200)  # Should remain on the form page

    def test_hero_list_pagination(self):
        # Create multiple heroes to fill more than one page
        for i in range(15):
            Hero.objects.create(
                name=f'Hero {i}', 
                body='A hero', 
                year_of_birth='1990',
                year_of_death='2023',
                nationality='Testland',
                user=self.user
            )
        response = self.client.get(reverse('heroes') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero 10')

    def test_hero_detail_view(self):
        hero = Hero.objects.create(
            name='Detail Hero', 
            body='A detailed hero', 
            year_of_birth='1990',
            year_of_death='1995',
            nationality='Testland',
            user=self.user
        )
        response = self.client.get(reverse('biography', args=[hero.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Hero')


class CommentTests(TestCase):

    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a hero instance
        self.hero = Hero.objects.create(
            name='Comment Hero', 
            body='A hero to comment on', 
            year_of_birth='1990',
            nationality='Testland',
            user=self.user
        )

    def test_authenticated_user_can_add_comment(self):
        # Log in the user
        self.client.login(username='testuser', password='password')
        
        # Post a comment
        response = self.client.post(reverse('biography', args=[self.hero.slug]), {
            'comment': 'This is a test comment.'
        })
        
        # Check if the response status code is a redirect (302)
        self.assertEqual(response.status_code, 302) 
        
        # Check if the comment was created
        self.assertTrue(Comment.objects.filter(comment='This is a test comment.').exists())
