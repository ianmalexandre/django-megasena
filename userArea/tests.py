from django.test import TestCase
from .views import createNewMegaSenaGame
import django
django.setup()
from django.test import TestCase
from userArea.models import User, Games
# Create your tests here.

class userMegaSena(TestCase):
    
    def test_generate_erro(self):
        ret = createNewMegaSenaGame(11)
        ret2 = createNewMegaSenaGame(5)

        self.assertEqual(ret, 'erro')
        self.assertEqual(ret2, 'erro')

    def test_generate_random_numbers(self):
        ret = createNewMegaSenaGame(6)
        length = len(ret)

        self.assertEqual(length, 6)
        typ = type(ret[0])

        self.assertEqual(typ, int)

        for i in ret:
            self.assertEqual((i < 61), True)
            self.assertEqual((i > 0), True)

class dbUse(TestCase):
    
    def setUp(self):
        user = User.objects.create(name="Jose", username="jose01", password="123456", salted_word="111111")
        Games.objects.create(numbers="10 20 30 40 50 60", user=user)

    def test1(self):
        user = User.objects.get(name="Jose")
        self.assertEqual(user.username, "jose01")
        
    def test2(self):
        user = User.objects.get(name="Jose")
        game = Games.objects.get(user=user)
        self.assertEqual(game.numbers, "10 20 30 40 50 60")
