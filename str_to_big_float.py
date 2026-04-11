from core import Big_float, normalized, BASE, random_BF, BF_to_str

def int_to_BF(number):
    return str_to_BF(str(number))


def str_to_BF(number_str):
    sign = find_sign(number_str)
    number_str = sign_processing(number_str)
    exp = calculate_exp(number_str)
    number_str = point_processing(number_str)
    mantissa = calculate_mantissa(number_str)
    num = Big_float(exp, mantissa, sign)
    num = normalized(num)
    return num


def find_sign(number_str):
    if number_str[0] == '-':
        return -1
    else:
        return 1


def sign_processing(number_str):
    if number_str[0] == '-':
        return number_str[1:]
    else:
        return number_str


def point_processing(number_str):
    point = number_str.find('.')
    if point != -1:
        return number_str[:point] + number_str[point + 1:]
    else:
        return number_str


def calculate_exp(number_str):
    index_of_point = number_str.find('.')
    if index_of_point != -1:
        exp = index_of_point - len(number_str) + 1
    else:
        exp = 0
    return exp


def calculate_mantissa(number_str):
    mantissa = []
    n = len(number_str)
    for i in range(n, 0, -BASE):
        start = max(0, i - BASE)
        mantissa.append(int(number_str[start:i]))
    return mantissa


if __name__ == '__main__':
    for _ in range(1):
        a = random_BF()
        b = BF_to_str(a)
        b = str_to_BF(b)
        print(BF_to_str(a))
        print()
        print(BF_to_str(b))
        print(a == b)
