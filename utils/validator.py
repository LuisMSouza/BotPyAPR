import re


def validate_email(email: str) -> bool:
    regExp = re.compile(
        r'^([\w\.\-]+)\@([a-z]+)\.([a-z]+\.)?(com|br|com\.br)$', flags=re.I)
    return True if regExp.match(email) else False


def validate_cpf(cpf: int | str) -> bool:
    regExp = re.compile(
        r'^(\d{3}\.?\d{3}\.?\d{3}-?\d{2})$')
    return True if regExp.match(f"{cpf}") else False
