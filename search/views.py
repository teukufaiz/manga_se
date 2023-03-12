from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.backends import UserModel
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FavoriteManga
import json

@login_required
def manga_list(request):
    with open('manga.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    manga_list = []
    for manga in data:
        genres = ''.join(manga['genres'])[1:-1]
        themes = ''.join(manga['themes'])[1:-1]
        demographics = ''.join(manga['demographics'])[1:-1]
        manga_data = {
            'manga_id': manga['manga_id'],
            'title': manga['title'],
            'score': manga['score'],
            'chapters': manga['chapters'],
            'genres': genres,
            'themes': themes,
            'demographics': demographics,
            'synopsis': manga['synopsis'],
            'main_picture': manga['main_picture'],
        }
        manga_list.append(manga_data)

    paginator = Paginator(manga_list, 33)
    page = request.GET.get('page')
    manga_list = paginator.get_page(page)

    context = {
        'manga_list': manga_list
    }

    return render(request, 'list.html', context)

@login_required
def manga_search(request):
    with open('manga.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    query = request.GET.get('q')

    filtered_manga_list = []
    for manga in data:
        # Mencari manga yang memiliki title atau synopsis mengandung query
        if query:
            if query.lower() in manga['title'].lower():
                # Jika query ditemukan, tambahkan manga ke dalam list
                genres = ''.join(manga['genres'])[1:-1]
                themes = ''.join(manga['themes'])[1:-1]
                demographics = ''.join(manga['demographics'])[1:-1]
                manga_data = {
                    'manga_id': manga['manga_id'],
                    'title': manga['title'],
                    'score': manga['score'],
                    'chapters': manga['chapters'],
                    'genres': genres,
                    'themes': themes,
                    'demographics': demographics,
                    'synopsis': manga['synopsis'],
                    'main_picture': manga['main_picture'],
                }

                filtered_manga_list.append(manga_data)

    
    paginator = Paginator(filtered_manga_list, 33)
    page = request.GET.get('page')
    filtered_manga_list = paginator.get_page(page)

    context = {
        'filtered_manga_list': filtered_manga_list,
        'query': query
    }
    
    return render(request, 'search.html', context)

@login_required
def manga_details(request, manga_id):
    with open('manga.json', 'r', encoding='utf-8') as f:
        manga_data = json.load(f)

    manga = next((m for m in manga_data if m['manga_id'] == manga_id), None)
    
    genres = ''.join(manga['genres'])[1:-1]
    themes = ''.join(manga['themes'])[1:-1]
    demographics = ''.join(manga['demographics'])[1:-1]
    manga_details = {
        'manga_id': manga['manga_id'],
        'title': manga['title'],
        'type': manga['type'],
        'score': manga['score'],
        'scored_by': manga['scored_by'],
        'status': manga['status'],
        'volumes': manga['volumes'],
        'chapters': manga['chapters'],
        'start_date': manga['start_date'],
        'end_date': manga['end_date'],
        'genres': genres,
        'themes': themes,
        'demographics': demographics,
        'synopsis': manga['synopsis'],
        'main_picture': manga['main_picture'],
        'url': manga['url'],
        'title_english': manga['title_english'],
        'title_japanese': manga['title_japanese'],
        'title_synonyms': manga['title_synonyms']
    }
    return render(request, 'manga_details.html', {'manga': manga_details})

@login_required
def favorite_manga(request):
    if request.user.is_authenticated:
        favorite_manga = FavoriteManga.objects.filter(user=request.user)
        manga_ids = [fm.manga_id for fm in favorite_manga]
        with open('manga.json', 'r', encoding='utf-8') as f:
            manga_data = json.load(f)
        favorite_manga_data = [m for m in manga_data if m['manga_id'] in manga_ids]

        manga_list = []
        for manga in favorite_manga_data:
            genres = ''.join(manga['genres'])[1:-1]
            themes = ''.join(manga['themes'])[1:-1]
            demographics = ''.join(manga['demographics'])[1:-1]
            manga_data = {
                'manga_id': manga['manga_id'],
                'title': manga['title'],
                'score': manga['score'],
                'chapters': manga['chapters'],
                'genres': genres,
                'themes': themes,
                'demographics': demographics,
                'synopsis': manga['synopsis'],
                'main_picture': manga['main_picture'],
            }
            manga_list.append(manga_data)

        paginator = Paginator(manga_list, 33)
        page = request.GET.get('page')
        manga_list = paginator.get_page(page)

        context = {
            'manga_list': manga_list
        }
        return render(request, 'favorite.html', {'favorite_manga': manga_list})
    else:
        return redirect('login')
    
@login_required
def add_favorite_manga(request):
    if request.method == 'POST':
        manga_id = request.POST.get('manga_id')
        favorite_manga = FavoriteManga(user=request.user, manga_id=manga_id)
        favorite_manga.save()
        return redirect('favorite_manga')
    else:
        return redirect('home')

@login_required
def remove_favorite_manga(request, manga_id):
    favorite_manga = FavoriteManga.objects.filter(user=request.user, manga_id=manga_id).first()
    if favorite_manga:
        favorite_manga.delete()
    return redirect('favorite_manga')

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('manga_list')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def registerUser(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def logoutUser(request):
	logout(request)
	return redirect('login')