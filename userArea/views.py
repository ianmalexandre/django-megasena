import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    JWTTokenUserAuthentication
)
from .permission import AdminOrItself

from django.contrib.auth import get_user_model
from .models import Games
from .serializers import GameModelSerializer
from .serializers import NewGameRequestSerializer
from .serializers import NewGameResponseSerializer
from .serializers import UserModelSerializer

User = get_user_model()
# Create your views here.
def createNewMegaSenaGame(numDezenas: int):
    if (numDezenas < 6 or numDezenas > 10):
        return "erro"
    return sorted([random.randint(1, 60) for _ in range(numDezenas)])

def requestGoogle():
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=opt)
    url = "https://www.google.com/search?q=caixa+mega+sena"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    valores = soup.find_all("span", class_='zSMazd UHlKbe')
    resultado = [valor.text for valor in valores]
    return resultado


def correctNumbers(response, actualGame):
    intersection = list(set(response) & set(actualGame))
    return len(intersection)

class GameVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            lastWinner = requestGoogle()
            lastGame = Games.objects.last()
            lastGame = GameModelSerializer(lastGame).data
            lastGameNumbers = lastGame['numbers'].replace('[', '').replace(']', '').split(',') 
            print(f'last winner = {lastWinner}, last game = {lastGameNumbers}')
            resp = {
                'acertos': correctNumbers(lastWinner, lastGameNumbers),
                'ultimo_ganhador': sorted(lastWinner),
                'seu_ultimo_jogo': sorted(lastGameNumbers)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class GamesAPIView(APIView, JWTTokenUserAuthentication):
    permission_classes=[IsAuthenticated]

    def get(self, request, format="None"):
        _, tokenData = self.authenticate(request)
        user = tokenData['user_id']
        user = User.objects.get(pk=user)

        queryset = Games.objects.filter(user=user)
        resp = GameModelSerializer(queryset, many=True)
        return Response(resp.data, status=status.HTTP_200_OK)

    def post(self, request, format="None"):
        _, tokenData = self.authenticate(request)
        user = tokenData['user_id']
        serializer = NewGameRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = serializer.data
            numbers = createNewMegaSenaGame(req['content'])
            user = User.objects.get(pk=user)
            queryset = Games.objects.create(numbers=numbers, user=user)
            response = GameModelSerializer(queryset)
            return Response(response.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'response': 'Corpo inválido'},
                        status=status.HTTP_400_BAD_REQUEST)

class UserAPIViewSet(APIView):
    permission_classes=[AdminOrItself]

    def get(self, request, pk=None, format=None):
        user = User.objects.get(pk=pk)
        serialize = UserModelSerializer(user)
        return Response(serialize.data, status=status.HTTP_200_OK)

class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes=[AdminOrItself]
    serializer_class = UserModelSerializer
    queryset = User.objects.all()