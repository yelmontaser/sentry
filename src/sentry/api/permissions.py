from sentry.constants import MEMBER_USER
from sentry.models import Team, Project


class PermissionError(Exception):
    pass


def has_perm(object, user, type=MEMBER_USER):
    if user.is_superuser:
        return True
    # TODO: abstract this into a permission registry
    if type(object) == Team:
        return object.slug in Team.objects.get_for_user(user)

    if hasattr(object, 'project'):
        object = object.project

    if type(object) == Project:
        return object.slug in Project.objects.get_for_user(user)

    raise TypeError(type(object))


def assert_perm(*args, **kwargs):
    if not has_perm(*args, **kwargs):
        raise PermissionError