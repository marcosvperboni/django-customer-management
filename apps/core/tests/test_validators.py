import pytest
from django.core.exceptions import ValidationError

from apps.core.validators import validate_cnpj, validate_cpf, validate_phone, validate_zip_code


@pytest.mark.parametrize("value", ["529.982.247-25", "52998224725"])
def test_validate_cpf_accepts_valid_document(value):
    validate_cpf(value)  # should not raise


@pytest.mark.parametrize("value", ["111.111.111-11", "123.456.789-00", "not-a-cpf"])
def test_validate_cpf_rejects_invalid_document(value):
    with pytest.raises(ValidationError):
        validate_cpf(value)


@pytest.mark.parametrize("value", ["11.222.333/0001-81", "11222333000181"])
def test_validate_cnpj_accepts_valid_document(value):
    validate_cnpj(value)


@pytest.mark.parametrize("value", ["11.111.111/1111-11", "not-a-cnpj"])
def test_validate_cnpj_rejects_invalid_document(value):
    with pytest.raises(ValidationError):
        validate_cnpj(value)


@pytest.mark.parametrize("value", ["11999998888", "+5511999998888"])
def test_validate_phone_accepts_valid_numbers(value):
    validate_phone(value)


@pytest.mark.parametrize("value", ["abc", "123"])
def test_validate_phone_rejects_invalid_numbers(value):
    with pytest.raises(ValidationError):
        validate_phone(value)


def test_validate_zip_code_accepts_valid_format():
    validate_zip_code("01310-100")


def test_validate_zip_code_rejects_invalid_format():
    with pytest.raises(ValidationError):
        validate_zip_code("invalid")
