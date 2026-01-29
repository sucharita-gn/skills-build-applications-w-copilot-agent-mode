from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all users.'))

        # Teams
        Team = self.get_or_create_team_model()
        Team.objects.all().delete()
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')
        self.stdout.write(self.style.SUCCESS('Created teams Marvel and DC.'))

        # Users (superheroes)
        users = [
            {'email': 'ironman@marvel.com', 'username': 'ironman', 'team': marvel},
            {'email': 'captain@marvel.com', 'username': 'captain', 'team': marvel},
            {'email': 'spiderman@marvel.com', 'username': 'spiderman', 'team': marvel},
            {'email': 'batman@dc.com', 'username': 'batman', 'team': dc},
            {'email': 'superman@dc.com', 'username': 'superman', 'team': dc},
            {'email': 'wonderwoman@dc.com', 'username': 'wonderwoman', 'team': dc},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='password', team=u['team'])
        self.stdout.write(self.style.SUCCESS('Created superhero users.'))

        # Activities
        Activity = self.get_or_create_activity_model()
        Activity.objects.all().delete()
        Activity.objects.create(user=User.objects.get(username='ironman'), type='run', duration=30, calories=300)
        Activity.objects.create(user=User.objects.get(username='batman'), type='cycle', duration=45, calories=400)
        self.stdout.write(self.style.SUCCESS('Created activities.'))

        # Workouts
        Workout = self.get_or_create_workout_model()
        Workout.objects.all().delete()
        Workout.objects.create(name='Pushups', description='Do 20 pushups')
        Workout.objects.create(name='Situps', description='Do 30 situps')
        self.stdout.write(self.style.SUCCESS('Created workouts.'))

        # Leaderboard
        Leaderboard = self.get_or_create_leaderboard_model()
        Leaderboard.objects.all().delete()
        Leaderboard.objects.create(user=User.objects.get(username='ironman'), score=1000)
        Leaderboard.objects.create(user=User.objects.get(username='batman'), score=900)
        self.stdout.write(self.style.SUCCESS('Created leaderboard.'))

        self.stdout.write(self.style.SUCCESS('Database population complete.'))

    def get_or_create_team_model(self):
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', 'Team')
        except LookupError:
            class Team(models.Model):
                name = models.CharField(max_length=100, unique=True)
                class Meta:
                    app_label = 'octofit_tracker'
            return Team

    def get_or_create_activity_model(self):
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', 'Activity')
        except LookupError:
            class Activity(models.Model):
                user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                type = models.CharField(max_length=50)
                duration = models.IntegerField()
                calories = models.IntegerField()
                class Meta:
                    app_label = 'octofit_tracker'
            return Activity

    def get_or_create_workout_model(self):
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', 'Workout')
        except LookupError:
            class Workout(models.Model):
                name = models.CharField(max_length=100)
                description = models.TextField()
                class Meta:
                    app_label = 'octofit_tracker'
            return Workout

    def get_or_create_leaderboard_model(self):
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', 'Leaderboard')
        except LookupError:
            class Leaderboard(models.Model):
                user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                score = models.IntegerField()
                class Meta:
                    app_label = 'octofit_tracker'
            return Leaderboard
