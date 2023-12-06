from django.conf import settings


def is_user_able(user, obj, action):
    role = user.groups.all().values_list('name', flat=True)
    if len(role) != 1:
        raise RuntimeError(f'{user} have more or less then one role')
    role = role[0]
    if role not in settings.ACCESS_MATRIX:
        raise RuntimeError(f'{user} have unexpected role: {role}')
    actions = settings.ACCESS_MATRIX[role].get(obj)
    if actions is None:
        raise RuntimeError(f'Object {obj} is unknown for this role: {role}')
    is_able = actions.get(action)
    if is_able is None:
        raise RuntimeError(f'Action {obj} is unknown for this role: {role} and action: {action}')
    return is_able == 1
