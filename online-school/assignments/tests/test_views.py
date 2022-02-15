from django.test import TestCase, Client
from django.urls import reverse
# from assignment.model
import json


class TestViews(TestCase):

    def test_project_hw_GET(self):
        client = Client()

        res = client.get(reverse("index"))

        self.assertEquals(res.status_code, 200)
