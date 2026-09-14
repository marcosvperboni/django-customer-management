import factory

from apps.core.validators import _check_digit
from apps.customers.models import Customer


def generate_valid_cpf(seed: int) -> str:
    base = f"{100000000 + seed:09d}"[-9:]
    first = _check_digit(base, list(range(10, 1, -1)))
    second = _check_digit(base + str(first), list(range(11, 1, -1)))
    return f"{base}{first}{second}"


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    full_name = factory.Sequence(lambda n: f"Customer {n}")
    document = factory.Sequence(generate_valid_cpf)
    email = factory.Sequence(lambda n: f"customer{n}@example.com")
    phone = "11999998888"
