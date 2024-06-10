import folium
import json

from django.utils import timezone
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)

def get_pokemon_image(request, image):
    return request.build_absolute_uri(image.url) if image else DEFAULT_IMAGE_URL


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    timezone_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=timezone_now,
        disappeared_at__gte=timezone_now
    )
    for pokemon_entity in pokemon_entities:
        image_url = get_pokemon_image(request, pokemon_entity.pokemon.image)
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        image_url = get_pokemon_image(request, pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    timezone_now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=timezone_now,
        disappeared_at__gte=timezone_now
    )
    image_url = get_pokemon_image(request, pokemon.image)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.lat, 
            pokemon_entity.lon, 
            image_url
        )

    previous_pokemon = pokemon.previous_evolution
    previous_evolution = {}
    if previous_pokemon:
        previous_evolution = {
            "title_ru": previous_pokemon.title,
            "pokemon_id": previous_pokemon.id,
            "img_url": get_pokemon_image(request, previous_pokemon.image)
        }
    
    next_pokemon = pokemon.next_evolutions.first()
    next_evolution = {}
    if next_pokemon:
        next_evolution = {
                "title_ru": next_pokemon.title,
                "pokemon_id": next_pokemon.id,
                "img_url": get_pokemon_image(request, next_pokemon.image)
            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': {
            'pokemon_id': pokemon.id,
            "img_url": image_url,
            "title_ru": pokemon.title,
            "title_en": pokemon.title_en,
            "title_jp": pokemon.title_jp,
            "description": pokemon.description,
            "previous_evolution": previous_evolution,
            "next_evolution": next_evolution
        }
    })