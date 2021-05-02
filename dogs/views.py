from django.shortcuts import render, redirect
from django.http import Http404
from requests.api import get
from .models import *
import requests
import random


def getFact():
    """
    https://github.com/DukeNgn/Dog-facts-API
    """
    endpoint = "http://dog-api.kinduff.com/api/facts?number=1"
    response = requests.get(endpoint).json()['facts'][0]
    
    return response


def fillDogs():
    """
    https://dog.ceo/dog-api/documentation/
    """
    Dogs.objects.all().delete()

    breeds_endpoint = "https://dog.ceo/api/breeds/list/all"
    breeds = list(requests.get(breeds_endpoint).json()['message'].keys())

    progresso = 0
    for breed in breeds:
        pic_endpoint = f"https://dog.ceo/api/breed/{breed}/images/random"
        pic = requests.get(pic_endpoint).json()['message']
        print(f"Carregando imagens. Progresso {progresso}/{len(breeds)}")
        Dogs(breed=breed, img_url=pic).save()
        progresso += 1


def get_token():
    endpoint = "https://api.petfinder.com/v2/oauth2/token"
    
    CLIENT_ID = "xzWW3rKRtyylDdinxEYEQ16c0ew3DVf0GW4ab07gTHNFGRuNCX"
    CLIENT_SEC = "tzTlgfJZKVpwJILe8OaQaJNMfU1HhvX5eFVB4iQH"

    payload = {
        'grant_type' : 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SEC
    }

    request = requests.post(endpoint, data=payload).json()
    print(request)

    return request['access_token']


def get_adoptions(token):
    strucutre = """
    https://api.petfinder.com/v2/{CATEGORY}/{ACTION}?{parameter_1}={value_1}&{parameter_2}={value_2}
    """
    #endpoint = "https://api.petfinder.com/v2/animals?type=dog&breed=akita"
    endpoint = "https://api.petfinder.com/v2/types"

    payload = {
        'Authorization': f'Bearer {token}'
    }

    request = requests.get(endpoint, params=payload)
    
    return request



# Create your views here.
def index(request):
    fun_fact = getFact()

    if request.method == 'POST':
        pass
    else:
        #fillDogs()
        print('---------------------------------------')
        print(get_adoptions(get_token()))
        print('---------------------------------------')
        all_dogs = Dogs.objects.all()
        return render(request, 'dogs/index.html', {'fun_fact': fun_fact, 'dogs': all_dogs})


def adoptions(request):
    return render(request, 'dogs/adoptions.html')