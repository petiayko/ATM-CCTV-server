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
        self.local_admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='LA')
        new_group.user_set.add(self.user)
        self.local_admin.force_login(self.user)

    def test_access(self):
        response = self.local_admin.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get('/accounts/information/')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get('/accounts/staff/')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.local_admin.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.local_admin.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.local_admin.get(f'/accounts/staff/{self.user.id}/password')
        self.assertEquals(response.status_code, 200)

        response = self.local_admin.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 404)

        response = self.local_admin.get('/accounts/logout/')
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
        self.network_admin = Client()

        self.user = User.objects.create_user(username='test', password='123')
        new_group, _ = models.Group.objects.get_or_create(name='NA')
        new_group.user_set.add(self.user)
        self.network_admin.force_login(self.user)

    def test_access(self):
        response = self.network_admin.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get('/accounts/information/')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get('/accounts/staff/')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get('/accounts/staff/add')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/accounts/staff/{user.id}/edit')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/accounts/staff/{user.id}/password')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.network_admin.get(f'/accounts/staff/{self.user.id}/password')
        self.assertEquals(response.status_code, 200)

        response = self.network_admin.get(f'/accounts/staff/{user.id}/delete')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/staff/')

        response = self.network_admin.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/accounts/login/')
