from django.conf import settings


def is_user_able(user, obj, action):
    for user_group in user.groups.all().values_list('name', flat=True):
        if user_group not in settings.ACCESS_MATRIX:
            continue
        if settings.ACCESS_MATRIX[user_group][obj].get(action, 0):
            return True
    return False
