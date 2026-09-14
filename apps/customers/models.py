from django.db import models

from apps.core.models import PartyModel
from apps.core.validators import validate_cpf


class Customer(PartyModel):
    full_name = models.CharField(max_length=150)
    document = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name
