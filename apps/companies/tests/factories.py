import factory

from apps.companies.models import Company
from apps.core.validators import _check_digit


def generate_valid_cnpj(seed: int) -> str:
    base = f"{10000000000 + seed:012d}"[-12:]
    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    first = _check_digit(base, first_weights)
    second = _check_digit(base + str(first), second_weights)
    return f"{base}{first}{second}"


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    trade_name = factory.Sequence(lambda n: f"Company {n}")
    legal_name = factory.Sequence(lambda n: f"Company {n} Ltda")
    cnpj = factory.Sequence(generate_valid_cnpj)
    email = factory.Sequence(lambda n: f"company{n}@example.com")
    phone = "11999998888"
