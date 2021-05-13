from django.db.models.fields import json
from django.shortcuts import render, redirect
from django.http import Http404
from requests.api import get
from .models import *
import requests
import difflib

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .serializers import AdoptionSerializer


@api_view(['GET', 'POST'])
def api_adoption(request, adoption_id):
    try:
        adoption = Adoption.objects.get(id=adoption_id)
    except Adoption.DoesNotExist:
        raise Http404()

    serialized_adoption = AdoptionSerializer(adoption)


    if request.method == 'POST':
        ID = int(str(request.path).split('/')[3])

    
    adoption = Adoption.objects.get(id=ID)
    
    if adoption.favorite == False:
        print('Ainda nãos estava nos favoritos')
        adoption.favorite = True
    else:
        print('Removido dos favoritos')
        adoption.favorite = False
    
    adoption.save()

    return Response(serialized_adoption.data)


class Doglovers():
    def __init__(self):
        self.load = False

    
    def getFact(self):
        """
        https://github.com/DukeNgn/Dog-facts-API
        """
        endpoint = "http://dog-api.kinduff.com/api/facts?number=1"
        response = requests.get(endpoint).json()['facts'][0]
        
        return response


    def fillDogs(self):
        """
        https://dog.ceo/dog-api/documentation/
        """
        Dogs.objects.all().delete()

        breeds_endpoint = "https://dog.ceo/api/breeds/list/all"
        breeds = list(requests.get(breeds_endpoint).json()['message'].keys())

        self.breeds_dogapi = breeds

        progresso = 0
        for breed in breeds:
            pic_endpoint = f"https://dog.ceo/api/breed/{breed}/images/random"
            pic = requests.get(pic_endpoint).json()['message']
            print(f"Carregando imagens. Progresso {progresso}/{len(breeds)}")
            Dogs(breed=breed, img_url=pic).save()
            progresso += 1
        
        self.load = False
    

    def get_token(self):
        endpoint = "https://api.petfinder.com/v2/oauth2/token"
        
        CLIENT_ID = "xzWW3rKRtyylDdinxEYEQ16c0ew3DVf0GW4ab07gTHNFGRuNCX"
        CLIENT_SEC = "tzTlgfJZKVpwJILe8OaQaJNMfU1HhvX5eFVB4iQH"

        payload = {
            'grant_type' : 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SEC
        }

        request = requests.post(endpoint, data=payload).json()

        return request['access_token']
    

    def fill_possible_breeds(self, token):
        """
        takes the possibles breeds from petfinder api
        """
        PossibleBreeds.objects.all().delete()
        endpoint = f"https://api.petfinder.com/v2/types/dog/breeds"

        payload = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(endpoint, headers=payload).json()['breeds']

        for dictionary in response:
            PossibleBreeds(breed=dictionary['name']).save()
        
    
    def correspondence(self):
        """
        Creat dict relating dogs breeds from DogApi with availables breeds in petfinder
        to do the requests
        """
        breeds_dogapi = []
        breeds_petfinder = []
        correspondence_breed = {}

        for element in Dogs.objects.all():
            breeds_dogapi.append(element.breed)

        for element in PossibleBreeds.objects.all():
            breeds_petfinder.append(element.breed)


        for element in breeds_dogapi:
            search_strings = []

            matches = difflib.get_close_matches(element, breeds_petfinder)
            
            for match in matches:
                search_strings.append("-".join(match.lower().split(" ")))

            correspondence_breed[element] = search_strings

        return {k : v for k,v in correspondence_breed.items() if v}
    

    def correspondence_data(self):
        """
        Create dict relating dogs breeds from DogApi, with the breed name from the 
        response of petfinder API
        """
        breeds_dogapi = []
        breeds_petfinder = []
        correspondence_breed = {}

        for element in Dogs.objects.all():
            breeds_dogapi.append(element.breed)

        for element in PossibleBreeds.objects.all():
            breeds_petfinder.append(element.breed)


        for element in breeds_dogapi:
            search_strings = []

            matches = difflib.get_close_matches(element, breeds_petfinder)
            
            for match in matches:
                search_strings.append(match)

            correspondence_breed[element] = search_strings

        return {k : v for k,v in correspondence_breed.items() if v}


    def get_adoptions(self, token, breed):

        endpoint = f"https://api.petfinder.com/v2/animals?type=dog&breed={breed}"

        payload = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(endpoint, headers=payload).json()['animals']

        return response


    def set_value(self, information):
        if information == None or information == "":
            return "Not Found"
        else:
            return information


    def fill_adoptions(self):
        Adoption.objects.all().delete()

        breeds_correspondence = self.correspondence()

        for values in breeds_correspondence.values():
            print(values)
            for v in values:
                print(v)
                json_response = self.get_adoptions(self.get_token(), v)
                
                for adoption in json_response:
                    try:
                        name = self.set_value(adoption['name'])
                        status = self.set_value(adoption['status'])
                        adoption_url = self.set_value(adoption['url'])
                        breed_primary = self.set_value(adoption['breeds']['primary'])
                        breed_secondary = self.set_value(adoption['breeds']['secondary'])
                        age = self.set_value(adoption['age'])
                        gender = self.set_value(adoption['gender'])
                        size = self.set_value(adoption['size'])
                        img_url = self.set_value(adoption['photos'][0]['medium'])
                        phone = self.set_value(adoption['contact']['phone'])
                        state = self.set_value(adoption['contact']['address']['state'])
                        city = self.set_value(adoption['contact']['address']['city'])
                        postcode = self.set_value(adoption['contact']['address']['postcode'])
                        adress = self.set_value(adoption['contact']['address']['address1'])

                        spayed_neutered = self.set_value(adoption['attributes']['spayed_neutered'])
                        house_trained = self.set_value(adoption['attributes']['house_trained'])
                        special_needs = self.set_value(adoption['attributes']['special_needs'])
                        shots_current = self.set_value(adoption['attributes']['shots_current'])

                        Adoption(name=name, status=status, adoption_url=adoption_url, breed_primary=breed_primary, breed_secondary=breed_secondary, 
                        age=age, gender=gender, size=size, img_url=img_url, phone=phone, state=state, city=city, postcode=postcode, adress=adress, 
                        spayed_neutered=spayed_neutered, house_trained=house_trained, special_needs=special_needs, shots_current=shots_current ).save()

                    except:
                        pass
                    
        self.load = False

    # Métodos de redenrização do que aparecerá na tela
    def index(self, request):
        fun_fact = self.getFact()

        if request.method == 'POST':
            update = request.POST.get('update')

            if update == 'update_photos':
                self.load = True
                self.fillDogs()
                
                if self.load:
                    return render(request, 'dogs/loading.html')

            if update == 'update_adoptions':
                self.load = True
                self.fill_adoptions()
                
                if self.load:
                    return render(request, 'dogs/loading.html')
            
            return redirect('index')
        else:
            #self.fill_possible_breeds(self.get_token())
            all_dogs = Dogs.objects.all()
            dogs_avalibles = self.correspondence_data()
            availables = []

            for dog in all_dogs:
                if dog.breed in dogs_avalibles.keys():
                    availables.append(dog)

            return render(request, 'dogs/index.html', {'fun_fact': fun_fact, 'dogs': availables})


    def adoptions(self, request, breed):
        all_adoptions = Adoption.objects.all()
        adoptions_breed = []

        possible_breeds = []
        breeds_correspondence = self.correspondence_data()

        for key, value in breeds_correspondence.items():
            if key == breed:
                possible_breeds = value

        for adoption in all_adoptions:
            if str(adoption.breed_primary) in possible_breeds or str(adoption.breed_secondary) in possible_breeds:
                adoptions_breed.append(adoption)

        return render(request, 'dogs/adoptions.html', {'breed': breed,  'adoptions': adoptions_breed})


    def favorites(self, request):
        favorites = []
        all_adoptions = Adoption.objects.all()

        for adoption in all_adoptions:
            if adoption.favorite == True:
                favorites.append(adoption)

        return render(request, 'dogs/favorites.html', {'adoptions': favorites})