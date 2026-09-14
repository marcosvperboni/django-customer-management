from django.db import models

from apps.core.models import PartyModel
from apps.core.validators import validate_cnpj


class Company(PartyModel):
    trade_name = models.CharField(max_length=150)
    legal_name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["trade_name"]
        verbose_name_plural = "companies"

    def __str__(self) -> str:
        return self.trade_name
