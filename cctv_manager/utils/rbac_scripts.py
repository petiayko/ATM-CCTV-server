from django.conf import settings


def is_user_able(user, obj, action):
    role = user.groups.all().values_list('name', flat=True)
    if len(role) != 1:
        raise RuntimeError(f'{user} have more or less then one role')
    role = role[0]
    if role not in settings.ACCESS_MATRIX:
        raise RuntimeError(f'{user} have unexpected role: {role}')
    return settings.ACCESS_MATRIX[role][obj].get(action, 0) == 1
