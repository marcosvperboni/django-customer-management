from __future__ import annotations

import re

from django.core.exceptions import ValidationError

phone_validator = re.compile(r"^\+?\d{8,15}$")


def validate_phone(value: str) -> None:
    if not phone_validator.match(value):
        raise ValidationError(
            "%(value)s is not a valid phone number. Use digits only, "
            "optionally prefixed with '+', 8-15 digits long.",
            params={"value": value},
        )


def validate_zip_code(value: str) -> None:
    if not re.match(r"^\d{5}-?\d{3}$", value):
        raise ValidationError(
            "%(value)s is not a valid ZIP code. Expected format: 00000-000.",
            params={"value": value},
        )


def _only_digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def _check_digit(digits: str, weights: list[int]) -> int:
    total = sum(int(d) * w for d, w in zip(digits, weights, strict=False))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def validate_cpf(value: str) -> None:
    digits = _only_digits(value)
    if len(digits) != 11 or digits == digits[0] * 11:
        raise ValidationError("%(value)s is not a valid CPF.", params={"value": value})

    first_check = _check_digit(digits[:9], list(range(10, 1, -1)))
    second_check = _check_digit(digits[:10], list(range(11, 1, -1)))

    if digits[9:11] != f"{first_check}{second_check}":
        raise ValidationError("%(value)s is not a valid CPF.", params={"value": value})


def validate_cnpj(value: str) -> None:
    digits = _only_digits(value)
    if len(digits) != 14 or digits == digits[0] * 14:
        raise ValidationError("%(value)s is not a valid CNPJ.", params={"value": value})

    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    first_check = _check_digit(digits[:12], first_weights)
    second_check = _check_digit(digits[:13], second_weights)

    if digits[12:14] != f"{first_check}{second_check}":
        raise ValidationError("%(value)s is not a valid CNPJ.", params={"value": value})
