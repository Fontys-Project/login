import factory
from loginapi.models import User, Role, Permission


class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: "user%d@mail.com" % n)
    # email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class RoleFactory(factory.Factory):
    name = factory.Sequence(lambda n: n)

    class Meta:
        model = Role


class PermissionFactory(factory.Factory):
    name = factory.Sequence(lambda n: n)

    class Meta:
        model = Permission
