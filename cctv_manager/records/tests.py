import os

from django.test import TestCase, Client
from django.contrib.auth import get_user_model, models

from .models import Record

User = get_user_model()


class TestUrlGuest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global record
        record = Record.objects.create(
            name='Запись тест',
            location='/data/cctv_manager/videos/rec.mp4',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        record.delete()

    def setUp(self):
        self.guest = Client()

    def test_access(self):
        response = self.guest.get('/archive/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/?next=/archive/')

        response = self.guest.get(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/archive/{record.id}/edit')

        response = self.guest.get(f'/archive/{record.id}/download')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/archive/{record.id}/download')

        response = self.guest.get(f'/archive/{record.id}/preview')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/archive/{record.id}/preview')

        response = self.guest.get(f'/archive/{record.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/archive/{record.id}/delete')


class TestUrlOperator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global record
        record = Record.objects.create(
            name='Запись тест',
            location=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'design/static/test/test.mp4')),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        record.delete()

    def setUp(self):
        self.operator = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='O')
        new_group.user_set.add(self.user)
        self.operator.force_login(self.user)

    def test_access(self):
        response = self.operator.get('/archive/')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 404)

        response = self.operator.post(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 404)

        response = self.operator.get(f'/archive/{record.id}/download')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/archive/{record.id}/preview')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/archive/{record.id}/delete')
        self.assertEquals(response.status_code, 404)


class TestUrlLocalAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global record
        record = Record.objects.create(
            name='Запись тест',
            location=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'design/static/test/test.mp4')),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        record.delete()

    def setUp(self):
        self.service = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='S')
        new_group.user_set.add(self.user)
        self.service.force_login(self.user)

    def test_access(self):
        response = self.service.get('/archive/')
        self.assertEquals(response.status_code, 200)

        response = self.service.get(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 404)

        response = self.service.post(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 404)

        response = self.service.get(f'/archive/{record.id}/download')
        self.assertEquals(response.status_code, 404)

        response = self.service.get(f'/archive/{record.id}/preview')
        self.assertEquals(response.status_code, 200)

        response = self.service.get(f'/archive/{record.id}/delete')
        self.assertEquals(response.status_code, 404)


class TestUrlNetworkAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global record
        record = Record.objects.create(
            name='Запись тест',
            location=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'design/static/test/test.mp4')),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        record.delete()

    def setUp(self):
        self.admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='A')
        new_group.user_set.add(self.user)
        self.admin.force_login(self.user)

    def test_access(self):
        response = self.admin.get('/archive/')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 405)

        response = self.admin.post(f'/archive/{record.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/archive/')

        response = self.admin.get(f'/archive/{record.id}/download')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/archive/{record.id}/preview')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/archive/{record.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/archive/')
