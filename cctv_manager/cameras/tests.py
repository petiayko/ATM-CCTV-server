from django.test import TestCase, Client
from django.contrib.auth import get_user_model, models

from cctv_manager.models import Camera

User = get_user_model()


class TestUrlGuest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global camera
        camera = Camera.objects.create(
            name='Камера тест',
            ip_address='15.80.132.14',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        camera.delete()

    def setUp(self):
        self.guest = Client()

    def test_access(self):
        response = self.guest.get('/cameras/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/?next=/cameras/')

        response = self.guest.get('/cameras/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/?next=/cameras/add')

        response = self.guest.get(f'/cameras/{camera.id}/detail')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/cameras/{camera.id}/detail')

        response = self.guest.get(f'/cameras/{camera.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/cameras/{camera.id}/edit')

        response = self.guest.get(f'/cameras/{camera.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/cameras/{camera.id}/delete')

        response = self.guest.get(f'/cameras/{camera.id}/ping')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/cameras/{camera.id}/ping')


class TestUrlOperator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global camera
        camera = Camera.objects.create(
            name='Камера тест',
            ip_address='15.80.132.14',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        camera.delete()

    def setUp(self):
        self.operator = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='O')
        new_group.user_set.add(self.user)
        self.operator.force_login(self.user)

    def test_access(self):
        response = self.operator.get('/cameras/')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get('/cameras/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/cameras/')

        response = self.operator.get(f'/cameras/{camera.id}/detail')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/cameras/{camera.id}/edit')
        self.assertEquals(response.status_code, 404)

        # response = self.operator.get(f'/cameras/{camera.id}/ping')
        # self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/cameras/{camera.id}/delete')
        self.assertEquals(response.status_code, 404)


class TestUrlLocalAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global camera
        camera = Camera.objects.create(
            name='Камера тест',
            ip_address='15.80.132.14',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        camera.delete()

    def setUp(self):
        self.local_admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='LA')
        new_group.user_set.add(self.user)
        self.local_admin.force_login(self.user)

    def test_access(self):
        response = self.local_admin.get('/cameras/')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get('/cameras/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/cameras/')

        response = self.local_admin.get(f'/cameras/{camera.id}/detail')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get(f'/cameras/{camera.id}/edit')
        self.assertEquals(response.status_code, 200)

        # response = self.local_admin.get(f'/cameras/{camera.id}/ping')
        # self.assertEquals(response.status_code, 200)

        response = self.local_admin.get(f'/cameras/{camera.id}/delete')
        self.assertEquals(response.status_code, 404)


class TestUrlNetworkAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global camera
        camera = Camera.objects.create(
            name='Камера тест',
            ip_address='15.80.132.14',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        camera.delete()

    def setUp(self):
        self.network_admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='NA')
        new_group.user_set.add(self.user)
        self.network_admin.force_login(self.user)

    def test_access(self):
        response = self.network_admin.get('/cameras/')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get('/cameras/add')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/cameras/{camera.id}/detail')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/cameras/{camera.id}/edit')
        self.assertEquals(response.status_code, 200)

        # response = self.network_admin.get(f'/cameras/{camera.id}/ping')
        # self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/cameras/{camera.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/cameras/')
