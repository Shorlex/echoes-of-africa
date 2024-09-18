from django.shortcuts import render
from heroes.models import Hero

def home_page(request):
    heroes = Hero.objects.all().order_by("-date")[:3]
    weekly_hero = Hero.objects.filter(hero_of_the_week=True).first()
    print(weekly_hero)
    context = {'heroes': heroes, 'weekly_hero': weekly_hero}
    return render(request, 'index.html', context)
