import re

def validate_id(id_number):
    return bool(re.fullmatch(r"\d{9}", id_number))

def validate_age(age):
    return 0 <= int(age) <= 120
