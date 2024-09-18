from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Hero, Comment, HeroImage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import HeroForm, CommentForm
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.
def heroes(request):
    query = request.GET.get('q')
    if query:
        heroes = Hero.objects.filter(
            Q(name__icontains=query) | 
            # Q(body__icontains=query) |
            Q(nationality__icontains=query)
        )
    else:
        heroes = Hero.objects.all().order_by("-date")
        paginator = Paginator(heroes, 8)

    # Apply pagination after filtering (whether query exists or not)
    paginator = Paginator(heroes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'query': query}
    return render(request, 'heroes/heroes.html', context)

def biography(request, slug):
    biography = Hero.objects.get(slug=slug)
    modified_name = biography.name.replace(' ', '<br>', 1)
    comments = biography.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.hero = biography
            new_comment.user = request.user
            #check if it a reply
            parent_id = request.POST.get('parent')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    new_comment.parent = parent_comment
                except:
                    pass
            new_comment.save()
            return redirect('biography', slug=biography.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'biography': biography,
        'name': modified_name,
        'comments': comments,
        'form': comment_form
    }
    return render(request, 'heroes/biography.html', context)

@login_required
def comment_like(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user_exist = comment.likes.filter(username=request.user.username).exists()
    if user_exist:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    
    return render(request, 'comment/likes.html', {'comment':comment}) 

@login_required
def post_hero(request):
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            new_hero = form.save(commit=False)
            new_hero.user = request.user
            new_hero.save()
            # Handle multiple hero images
            # if request.FILES.getlist('images'):
            #     for image in request.FILES.getlist('images'):
            #         HeroImage.objects.create(hero=new_hero, image=image)

            #Save hero images
            for image in images:
                HeroImage.objects.create(hero=new_hero, image=image)

            return redirect('heroes')
        else:
            print(form.errors)
    else:
        form = HeroForm()

    context = {'form': form}
    return render(request, 'heroes/post_hero.html', context)

@login_required
def update_hero(request, slug):
    biography = Hero.objects.get(slug=slug)
    images = request.FILES.getlist('images')
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=biography)
        if form.is_valid():
            form.save()

            for image in images:
                HeroImage.objects.create(hero=biography, image=image)
            return redirect('biography', slug = biography.slug)
    else:
        form = HeroForm(instance=biography)
    
    context = {'form': form}
    return render(request, 'heroes/update_hero.html', context)

@login_required
def delete_hero(request, slug):
    biography = Hero.objects.get(slug=slug)
    if request.method == "POST":
        biography.delete()
        return redirect('heroes')

    return HttpResponseRedirect(reverse('biography', args=[biography.slug]))