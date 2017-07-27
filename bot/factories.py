import factory
from faker import Factory

fake = Factory.create()


class UserFactory(factory.Factory):
    first_name = factory.LazyFunction(lambda: fake.name().split()[0])
    last_name = factory.LazyFunction(lambda: fake.name().split()[1])
    email = factory.LazyAttribute(
        lambda obj: 'info+{}@light-it.net'.format(obj.first_name)
    )
    password = factory.LazyAttribute(
        lambda obj: '{}-{}'.format(obj.first_name, obj.last_name)
    )


class PostFactory(factory.Factory):
    text = factory.Faker('text')
