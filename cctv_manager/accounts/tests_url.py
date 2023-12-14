from django.test import TestCase, Client
from django.contrib.auth import get_user_model, models

User = get_user_model()


class TestUrlGuest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global user
        user = User.objects.create(
            username='Тест',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        user.delete()

    def setUp(self):
        self.guest = Client()

    def test_access(self):
        response = self.guest.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.guest.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/')

        response = self.guest.get('/accounts/information/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/information/')

        response = self.guest.get('/accounts/staff/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/staff/')

        response = self.guest.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/staff/add')

        response = self.guest.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/staff/{user.id}/delete')

        response = self.guest.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/staff/{user.id}/edit')

        response = self.guest.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f'/accounts/login/?next=/accounts/staff/{user.id}/password')


class TestUrlOperator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global user
        user = User.objects.create(
            username='Тест',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        user.delete()

    def setUp(self):
        self.operator = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='O')
        new_group.user_set.add(self.user)
        self.operator.force_login(self.user)

    def test_access(self):
        response = self.operator.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get('/accounts/information/')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get('/accounts/staff/')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.operator.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.operator.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.operator.get(f'/accounts/staff/{self.user.id}/password')
        self.assertEquals(response.status_code, 200)

        response = self.operator.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 404)

        response = self.operator.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/')


class TestUrlLocalAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global user
        user = User.objects.create(
            username='Тест',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        user.delete()

    def setUp(self):
        self.service = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='S')
        new_group.user_set.add(self.user)
        self.service.force_login(self.user)

    def test_access(self):
        response = self.service.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.service.get('/accounts/information/')
        self.assertEquals(response.status_code, 200)

        response = self.service.get('/accounts/staff/')
        self.assertEquals(response.status_code, 200)

        response = self.service.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.service.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.service.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.service.get(f'/accounts/staff/{self.user.id}/password')
        self.assertEquals(response.status_code, 200)

        response = self.service.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 404)

        response = self.service.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/')


class TestUrlNetworkAdministrator(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        global user
        user = User.objects.create(
            username='Тест',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        user.delete()

    def setUp(self):
        self.admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='A')
        new_group.user_set.add(self.user)
        self.admin.force_login(self.user)

    def test_access(self):
        response = self.admin.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get('/accounts/information/')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get('/accounts/staff/')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.admin.get(f'/accounts/staff/{self.user.id}/password')
        self.assertEquals(response.status_code, 200)

        response = self.admin.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.admin.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/')
