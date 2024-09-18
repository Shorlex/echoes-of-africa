from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class Hero(models.Model):
    name = models.CharField(max_length=75)
    body = models.TextField()
    year_of_birth = models.IntegerField()
    year_of_death = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    nationality = models.CharField(max_length=75)
    banner = models.ImageField(upload_to='heroes_banner/', default='default.png')
    slug = models.SlugField(blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hero')
    hero_of_the_week = models.BooleanField(default=False)
    date_selected = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Hero.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        
        if self.hero_of_the_week:
            # Set hero_of_the_week to False for all other heroes
            Hero.objects.filter(hero_of_the_week=True).update(hero_of_the_week=False)
        super().save(*args, **kwargs)

class HeroImage(models.Model):
    hero = models.ForeignKey(Hero, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='heroes_images/')
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.hero.name}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    hero = models.ForeignKey(Hero, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, through="CommentLike")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username}"
    
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user} on {self.comment}'
    
