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
        pass

    def getSealToken(self):
        username = "leonardodma"
        endpoint = f"http://54.88.109.168/{username}/token"
        response = requests.get(endpoint).json()['token']

        return response


    def createSeal(self, token):
        username = "leonardodma"
        endpoint = f"http://54.88.109.168/{username}/image"

        #headers = {'Content-type': 'application/json'}
        payload = {"token": token}
        #data = payload.dumps(payload)

        request = requests.post(endpoint, json=payload).json()['image_uri']

        return request
    
    def getSealSrc(self, img_name):
        src = "http://54.88.109.168"+img_name
        return src


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


    def updatePicture(self, breed):
        pic_endpoint = f"https://dog.ceo/api/breed/{breed}/images/random"
        pic = requests.get(pic_endpoint).json()['message']
        dog = Dogs.objects.get(breed=breed)
        dog.img_url = pic
        dog.save()
    

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


        for element in sorted(breeds_dogapi):
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


    def fill_adoptions_breed(self, breed):
        #Adoption.objects.get(id=ID)
        #Adoption.objects.all().delete()

        breeds_correspondence = self.correspondence()
        print(f'Correspondência com string de pesquisa do endpoint: {breeds_correspondence}')
        print('\n\n')
        data_correspondence = self.correspondence_data()
        print(f'Correspondência dados da resposta da API: {data_correspondence}')


        
        Adoption.objects.filter(breed_primary__in=data_correspondence[breed]).delete()
        Adoption.objects.filter(breed_secondary__in=data_correspondence[breed]).delete()
        
        for value in breeds_correspondence[breed]:
            print(value)

            json_response = self.get_adoptions(self.get_token(), value)
                
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
            
                
    # Métodos de redenrização do que aparecerá na tela
    def index(self, request):
        token = self.getSealToken()
        print("-----------------------------------")
        print(f"TOKEN: {token}")
        print("-----------------------------------")
        img_name = self.createSeal(token)
        seal_src = self.getSealSrc(img_name)
        print("-----------------------------------")
        print(f"IMG_SRC: {seal_src}")
        print("-----------------------------------")


        fun_fact = self.getFact()

        if request.method == 'POST':
            breed = request.POST.get('update_pic')
            self.updatePicture(breed)

            return redirect('index')

        if not Dogs.objects.exists():
            self.fill_possible_breeds(self.get_token())
            self.fillDogs()

        all_dogs = Dogs.objects.all().order_by("breed")
        dogs_avalibles = self.correspondence_data()


        availables = []

        for dog in all_dogs:
            if dog.breed in dogs_avalibles.keys():
                availables.append(dog)

        return render(request, 'dogs/index.html', {'fun_fact': fun_fact, 'dogs': availables, 'seal_src':seal_src})


    def adoptions(self, request, breed):

        if request.method == 'POST':
            update = request.POST.get('update')
            print(update)

            if update == 'update_adoptions':
                self.fill_possible_breeds(self.get_token())
                self.fill_adoptions_breed(breed)

            return redirect('adoptions', breed)


        all_adoptions = Adoption.objects.all().order_by("name")
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