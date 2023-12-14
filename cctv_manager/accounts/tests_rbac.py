from django.test import TestCase
from django.contrib.auth import get_user_model, models
from django.conf import settings

from utils.rbac_scripts import is_user_able

User = get_user_model()


class TestAccessMatrixStruct(TestCase):
    def setUp(self):
        self.access_matrix = settings.ACCESS_MATRIX

    def test_groups_name(self):
        self.assertListEqual(list(self.access_matrix.keys()), ['A', 'S', 'O'])

    def test_objects_name(self):
        self.assertListEqual(list(self.access_matrix['A'].keys()), ['C', 'R', 'U'])
        self.assertListEqual(list(self.access_matrix['S'].keys()), ['C', 'R', 'U'])
        self.assertListEqual(list(self.access_matrix['O'].keys()), ['C', 'R', 'U'])

    def test_actions_name(self):
        self.assertListEqual(list(self.access_matrix['A']['C']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['S']['C']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['O']['C']), ['C', 'E', 'D', 'S', 'A'])

        self.assertListEqual(list(self.access_matrix['A']['R']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['S']['R']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['O']['R']), ['C', 'E', 'D', 'S', 'A'])

        self.assertListEqual(list(self.access_matrix['A']['U']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['S']['U']), ['C', 'E', 'D', 'S', 'A'])
        self.assertListEqual(list(self.access_matrix['O']['U']), ['C', 'E', 'D', 'S', 'A'])


class TestRbacOperator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='O')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertFalse(is_user_able(self.user, 'C', 'C'))
        self.assertFalse(is_user_able(self.user, 'C', 'E'))
        self.assertFalse(is_user_able(self.user, 'C', 'D'))
        self.assertFalse(is_user_able(self.user, 'C', 'S'))
        self.assertFalse(is_user_able(self.user, 'C', 'A'))

    def test_is_user_able_record(self):
        self.assertTrue(is_user_able(self.user, 'R', 'C'))
        self.assertFalse(is_user_able(self.user, 'R', 'E'))
        self.assertFalse(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'S'))
        self.assertTrue(is_user_able(self.user, 'R', 'A'))

    def test_is_user_able_staff(self):
        self.assertFalse(is_user_able(self.user, 'U', 'C'))
        self.assertFalse(is_user_able(self.user, 'U', 'E'))
        self.assertFalse(is_user_able(self.user, 'U', 'D'))
        self.assertFalse(is_user_able(self.user, 'U', 'S'))
        self.assertFalse(is_user_able(self.user, 'U', 'A'))


class TestRbacService(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='S')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertFalse(is_user_able(self.user, 'C', 'C'))
        self.assertFalse(is_user_able(self.user, 'C', 'E'))
        self.assertFalse(is_user_able(self.user, 'C', 'D'))
        self.assertTrue(is_user_able(self.user, 'C', 'S'))
        self.assertTrue(is_user_able(self.user, 'C', 'A'))

    def test_is_user_able_record(self):
        self.assertFalse(is_user_able(self.user, 'R', 'C'))
        self.assertFalse(is_user_able(self.user, 'R', 'E'))
        self.assertFalse(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'S'))
        self.assertFalse(is_user_able(self.user, 'R', 'A'))

    def test_is_user_able_staff(self):
        self.assertFalse(is_user_able(self.user, 'U', 'C'))
        self.assertFalse(is_user_able(self.user, 'U', 'E'))
        self.assertFalse(is_user_able(self.user, 'U', 'D'))
        self.assertFalse(is_user_able(self.user, 'U', 'S'))
        self.assertFalse(is_user_able(self.user, 'U', 'A'))


class TestRbacAdministrator(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='A')
        new_group.user_set.add(self.user)

    def test_is_user_able_camera(self):
        self.assertTrue(is_user_able(self.user, 'C', 'C'))
        self.assertTrue(is_user_able(self.user, 'C', 'E'))
        self.assertTrue(is_user_able(self.user, 'C', 'D'))
        self.assertTrue(is_user_able(self.user, 'C', 'S'))
        self.assertTrue(is_user_able(self.user, 'C', 'A'))

    def test_is_user_able_record(self):
        self.assertTrue(is_user_able(self.user, 'R', 'C'))
        self.assertTrue(is_user_able(self.user, 'R', 'E'))
        self.assertTrue(is_user_able(self.user, 'R', 'D'))
        self.assertTrue(is_user_able(self.user, 'R', 'S'))
        self.assertTrue(is_user_able(self.user, 'R', 'A'))

    def test_is_user_able_staff(self):
        self.assertTrue(is_user_able(self.user, 'U', 'C'))
        self.assertTrue(is_user_able(self.user, 'U', 'E'))
        self.assertTrue(is_user_able(self.user, 'U', 'D'))
        self.assertTrue(is_user_able(self.user, 'U', 'S'))
        self.assertFalse(is_user_able(self.user, 'U', 'A'))


class TestRbacNoRoleUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_is_user_able(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'E')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'S')
            is_user_able(self.user, 'C', 'A')

            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'E')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'S')
            is_user_able(self.user, 'R', 'A')

            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'E')
            is_user_able(self.user, 'U', 'D')
            is_user_able(self.user, 'U', 'S')
            is_user_able(self.user, 'U', 'A')


class TestRbacFewRolesUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='A')
        new_group.user_set.add(self.user)
        new_group, _ = models.Group.objects.get_or_create(name='S')
        new_group.user_set.add(self.user)

    def test_is_user_able(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'E')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'S')
            is_user_able(self.user, 'C', 'A')

            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'E')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'S')
            is_user_able(self.user, 'R', 'A')

            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'E')
            is_user_able(self.user, 'U', 'D')
            is_user_able(self.user, 'U', 'S')
            is_user_able(self.user, 'U', 'A')


class TestRbacUnknownRoleActionObject(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        new_group, _ = models.Group.objects.get_or_create(name='TG')
        new_group.user_set.add(self.user)

        self.user1 = User.objects.create_user(username='test1')

    def test_is_user_able_unknown_role(self):
        with self.assertRaises(RuntimeError):
            is_user_able(self.user, 'C', 'C')
            is_user_able(self.user, 'C', 'E')
            is_user_able(self.user, 'C', 'D')
            is_user_able(self.user, 'C', 'S')
            is_user_able(self.user, 'C', 'A')

            is_user_able(self.user, 'R', 'C')
            is_user_able(self.user, 'R', 'E')
            is_user_able(self.user, 'R', 'D')
            is_user_able(self.user, 'R', 'S')
            is_user_able(self.user, 'R', 'A')

            is_user_able(self.user, 'U', 'C')
            is_user_able(self.user, 'U', 'E')
            is_user_able(self.user, 'U', 'D')
            is_user_able(self.user, 'U', 'S')
            is_user_able(self.user, 'U', 'A')

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
