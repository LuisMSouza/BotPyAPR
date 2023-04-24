import re


def validate_email(email: str) -> bool:
    regExp = re.compile(
        r'^([\w]+)\@([a-z]+)\.([a-z]+\.)?(com|com\.br|br)$', flags=re.I)
    return True if regExp.match(email) != None else False


def validate_cpf(cpf: int) -> bool:
    regExp = re.compile(r'^([\d]{11})$')
    return True if regExp.match(cpf) != None else False
