from django.test import TestCase, Client
from django.contrib.auth import get_user_model, models
from django.conf import settings

from utils.rbac_scripts import is_user_able

User = get_user_model()


class TestAccessMatrixStruct(TestCase):
    def setUp(self):
        self.access_matrix = settings.ACCESS_MATRIX

    def test_groups_name(self):
        self.assertListEqual(list(self.access_matrix.keys()), ['NA', 'LA', 'O'])

    def test_objects_name(self):
        self.assertListEqual(list(self.access_matrix['NA'].keys()), ['C', 'R', 'U'])
        self.assertListEqual(list(self.access_matrix['LA'].keys()), ['C', 'R', 'U'])
        self.assertListEqual(list(self.access_matrix['O'].keys()), ['C', 'R', 'U'])

    def test_actions_name(self):
        self.assertListEqual(list(self.access_matrix['NA']['C']), ['A', 'C', 'D', 'R'])
        self.assertListEqual(list(self.access_matrix['LA']['C']), ['A', 'C', 'D', 'R'])
        self.assertListEqual(list(self.access_matrix['O']['C']), ['A', 'C', 'D', 'R'])

        self.assertListEqual(list(self.access_matrix['NA']['R']), ['A', 'C', 'D', 'L'])
        self.assertListEqual(list(self.access_matrix['LA']['R']), ['A', 'C', 'D', 'L'])
        self.assertListEqual(list(self.access_matrix['O']['R']), ['A', 'C', 'D', 'L'])

        self.assertListEqual(list(self.access_matrix['NA']['U']), ['A', 'C', 'D'])
        self.assertListEqual(list(self.access_matrix['LA']['U']), ['A', 'C', 'D'])
        self.assertListEqual(list(self.access_matrix['O']['U']), ['A', 'C', 'D'])


class TestRbacOperator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='O')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertFalse(is_user_able(self.user, 'C', 'A'))
        self.assertFalse(is_user_able(self.user, 'C', 'C'))
        self.assertFalse(is_user_able(self.user, 'C', 'D'))
        self.assertFalse(is_user_able(self.user, 'C', 'R'))

    def test_is_user_able_record(self):
        self.assertTrue(is_user_able(self.user, 'R', 'A'))
        self.assertFalse(is_user_able(self.user, 'R', 'C'))
        self.assertFalse(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'L'))

    def test_is_user_able_staff(self):
        self.assertFalse(is_user_able(self.user, 'U', 'A'))
        self.assertFalse(is_user_able(self.user, 'U', 'C'))
        self.assertFalse(is_user_able(self.user, 'U', 'D'))

    def tearDown(self):
        self.user.delete()


class TestRbacLocalAdministrator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='LA')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertFalse(is_user_able(self.user, 'C', 'A'))
        self.assertTrue(is_user_able(self.user, 'C', 'C'))
        self.assertFalse(is_user_able(self.user, 'C', 'D'))
        self.assertTrue(is_user_able(self.user, 'C', 'R'))

    def test_is_user_able_record(self):
        self.assertTrue(is_user_able(self.user, 'R', 'A'))
        self.assertFalse(is_user_able(self.user, 'R', 'C'))
        self.assertFalse(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'L'))

    def test_is_user_able_staff(self):
        self.assertFalse(is_user_able(self.user, 'U', 'A'))
        self.assertFalse(is_user_able(self.user, 'U', 'C'))
        self.assertFalse(is_user_able(self.user, 'U', 'D'))

    def tearDown(self):
        self.user.delete()


class TestRbacNetworkAdministrator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='NA')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertTrue(is_user_able(self.user, 'C', 'A'))
        self.assertTrue(is_user_able(self.user, 'C', 'C'))
        self.assertTrue(is_user_able(self.user, 'C', 'D'))
        self.assertTrue(is_user_able(self.user, 'C', 'R'))

    def test_is_user_able_record(self):
        self.assertTrue(is_user_able(self.user, 'R', 'A'))
        self.assertTrue(is_user_able(self.user, 'R', 'C'))
        self.assertTrue(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'L'))

    def test_is_user_able_staff(self):
        self.assertTrue(is_user_able(self.user, 'U', 'A'))
        self.assertTrue(is_user_able(self.user, 'U', 'C'))
        self.assertTrue(is_user_able(self.user, 'U', 'D'))

    def tearDown(self):
        self.user.delete()


class TestRbacNoRoleUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_is_user_able(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'A')
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'R')

            is_user_able(self.user, 'R', 'A')
            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'L')

            is_user_able(self.user, 'U', 'A')
            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'D')

    def tearDown(self):
        self.user.delete()


class TestRbacFewRolesUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='NA')
        new_group.user_set.add(self.user)
        new_group, _ = models.Group.objects.get_or_create(name='LA')
        new_group.user_set.add(self.user)

    def test_is_user_able(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'A')
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'R')

            is_user_able(self.user, 'R', 'A')
            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'L')

            is_user_able(self.user, 'U', 'A')
            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'D')

    def tearDown(self):
        self.user.delete()


class TestRbacUnknownRoleActionObject(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='TG')
        new_group.user_set.add(self.user)

        self.user1 = User.objects.create_user(username='test1')

    def test_is_user_able_unknown_role(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'A')
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'R')

            is_user_able(self.user, 'R', 'A')
            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'L')

            is_user_able(self.user, 'U', 'A')
            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'D')

    def test_is_user_able_unknown_action(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user1, 'C', 'B')
            is_user_able(self.user1, 'C', 'T')
            is_user_able(self.user1, 'C', 'Y')
            is_user_able(self.user1, 'C', 'I')

            is_user_able(self.user1, 'R', 'Q')
            is_user_able(self.user1, 'R', 'W')
            is_user_able(self.user1, 'R', 'X')
            is_user_able(self.user1, 'R', 'Z')

            is_user_able(self.user1, 'U', 'B')
            is_user_able(self.user1, 'U', 'N')
            is_user_able(self.user1, 'U', 'M')

    def test_is_user_able_unknown_object(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user1, 'V', 'B')
            is_user_able(self.user1, 'L', 'T')
            is_user_able(self.user1, 'P', 'Y')
            is_user_able(self.user1, 'O', 'I')

    def tearDown(self):
        self.user.delete()
        self.user1.delete()
