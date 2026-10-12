


def is_valid_oib(oib: int) -> bool:
    string_oib=str(oib)
    if len(string_oib)!=11 or oib==None:
        return False
    a = 10
    for digit_char in string_oib[:10]:
        a = (a + int(digit_char)) % 10
        if a == 0:
            a = 10
        a = (a * 2) % 11

    control_digit = 11 - a
    if control_digit == 10:
        control_digit = 0

    return control_digit == int(string_oib[10])


