import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from heroes.models import Hero

class Command(BaseCommand):
    help = 'Update Hero of the Week'

    def handle(self, *args, **kwargs):
        # Set all heroes to not be "Hero of the Week"
        Hero.objects.update(hero_of_the_week=False)

        # Select a random hero
        heroes = Hero.objects.all()
        if heroes.exists():
            hero_of_the_week = random.choice(heroes)
            hero_of_the_week.hero_of_the_week = True
            hero_of_the_week.date_selected = timezone.now()
            hero_of_the_week.save()
            self.stdout.write(self.style.SUCCESS(f'{hero_of_the_week.name} is now the Hero of the Week!'))
        else:
            self.stdout.write(self.style.WARNING('No heroes found!'))
