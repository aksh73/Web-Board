from django.http import HttpRequest
from django.urls import reverse
from django.test import SimpleTestCase
from .views import home, board_topics
# from . import views
# from .models import Board

class HomeTests(SimpleTestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

# class BoardTopicsTests(TestCase):
#     def setUp(self):
#         Board.objects.create(name='Django', description='Django board.')
#
#     def test_board_topics_view_success_status_code(self):
#         url = reverse('board_topics', kwargs={'pk': 1})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_board_topics_view_not_found_status_code(self):
#         url = reverse('board_topics', kwargs={'pk': 99})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)
#
#     def test_board_topics_url_resolves_board_topics_view(self):
#         view = resolve('/boards/1/')
#         self.assertEquals(view.func, board_topics)
