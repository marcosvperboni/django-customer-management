import datetime

import factory
from django.utils import timezone

from apps.crm.models import Address, Contact, Document, Observation, RelationshipHistory, Task
from apps.customers.tests.factories import CustomerFactory


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    customer = factory.SubFactory(CustomerFactory)
    full_name = factory.Sequence(lambda n: f"Contact {n}")
    email = factory.Sequence(lambda n: f"contact{n}@example.com")
    phone = "11999998888"


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    street = "Av. Paulista"
    number = "1000"
    neighborhood = "Bela Vista"
    city = "Sao Paulo"
    state = "SP"
    zip_code = "01310-100"


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    customer = factory.SubFactory(CustomerFactory)
    title = factory.Sequence(lambda n: f"Document {n}")
    file = factory.django.FileField(filename="document.pdf")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    customer = factory.SubFactory(CustomerFactory)
    title = factory.Sequence(lambda n: f"Task {n}")
    due_date = factory.LazyFunction(lambda: datetime.date.today() + datetime.timedelta(days=7))


class RelationshipHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelationshipHistory

    customer = factory.SubFactory(CustomerFactory)
    interaction_type = "CALL"
    description = "Discussed contract renewal."
    occurred_at = factory.LazyFunction(timezone.now)


class ObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Observation

    customer = factory.SubFactory(CustomerFactory)
    content = "Prefers email over phone calls."
