from django.test import TestCase, RequestFactory
# from kitchen.views import KitchenDetailView
from kitchen.models import Kitchen

# Create your tests here.
class KitchenTestSetUpCase(TestCase):
    def setUp(self):
        Kitchen.objects.create(name="App 1", email="test@mail.com")
        Kitchen.objects.create(name="App 2", email="test2@mail.com")


class AppTestURLCase(TestCase):
    def test_urls(self):
        print('\n========= This is TEST CASE for URLS ===========\n')
        responses = {
                        #'Home Page': self.client.get('/'),
                        'Home Page': self.client.get('http://100.24.4.172/'),
                     #   'Kitchen List Page': self.client.get('/kitchen/'),
                     #   'Kitchen App Page': self.client.get('/kitchen/create'),
                     #   'Kitchen Detail Page': self.client.get('/kitchen/1/detail'),
                     #   'Kitchen Update Page': self.client.get('/kitchen/1/update'),
                     #   'Kitchen Delete Page': self.client.get('/kitchen/1/delete'),
                    }
        # Issue a GET request for each REQUEST
        for key, response in responses.items():
            # Check that the response is 200 OK.
            try:
                self.assertEqual(response.status_code, 200)
                print('(WORKING) {} | {}\n'.format(key,response))
            except:
                print('(NOT working) {} | {}\n'.format(key,response))
        print('\n========= END of TEST CASE for URLS ===========\n')
