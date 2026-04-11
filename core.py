from random import randrange, choice

BASE = 5


class Big_float:
    __slots__ = ('exp', 'mantissa', 'sign')
    def __init__(self, exp=0, mantissa=[0], sign=1):
        self.exp = exp
        self.mantissa = mantissa[:]
        self.sign = sign

    def set_sign(self, sign):
        self.sign = sign

    def set_exp(self, exp):
        self.exp = exp

    def set_mantissa(self, mantissa):
        self.mantissa = mantissa

    def get_sign(self):
        return self.sign

    def get_exp(self):
        return self.exp

    def get_mantissa(self):
        return self.mantissa.copy()


def random_BF():
    mantissa = []
    exp = randrange(-10000, 0)
    prec = choice([2000, 1999])
    for _ in range(prec):
        elem = randrange(1000, 10000)
        mantissa.append(elem)
    sign = choice([1, -1])
    return normalized(Big_float(exp, mantissa, sign))


def big_float_copy(big_float_num):
    exp = big_float_num.get_exp()
    sign = big_float_num.get_sign()
    mantissa = big_float_num.get_mantissa()
    return Big_float(exp, mantissa, sign)


def BF_round(num, precision):
    mantissa = num.get_mantissa()
    exp = num.get_exp()
    old_len = len(mantissa)
    if old_len < precision:
        return num
    mantissa = mantissa[-precision:]
    exp = exp + (old_len - len(mantissa)) * BASE
    num = Big_float(exp, mantissa, num.get_sign())
    return num


def normalized(big_float_num):
    mantissa = big_float_num.get_mantissa()
    sign = big_float_num.get_sign()
    new_exp = big_float_num.get_exp()
    len_old_mantissa = len(mantissa)
    if mantissa_is_zero(mantissa):
        return make_zero(mantissa)
    else:
        if mantissa_starts_with_zero(mantissa):
            mantissa = strip_leading_zeros(mantissa)
            new_exp = adjust_exp_after_strip(big_float_num, len_old_mantissa, mantissa)
        if mantissa_ends_with_zero(mantissa):
            mantissa = strip_trailing_zeros(mantissa)
    return Big_float(new_exp, mantissa, sign)


def BF_to_str(big_float_num):
    mantissa = big_float_num.get_mantissa()
    exp = big_float_num.get_exp()
    sign = big_float_num.get_sign()
    big_num_str = mantissa_to_str(mantissa)
    if exp < 0:
        big_num_str = insert_point(big_num_str, exp)
    elif exp > 0:
        big_num_str = insert_zeros(big_num_str, exp)
    if sign == -1:
        big_num_str = insert_sign(big_num_str)
    return big_num_str


def insert_point(mantissa_str, exp):
    if abs(exp) > len(mantissa_str):
        mantissa_str = '0.' + '0' * (abs(exp) - len(mantissa_str)) + mantissa_str
    elif abs(exp) == len(mantissa_str):
        mantissa_str = '0.' + mantissa_str
    else:
        mantissa_str = mantissa_str[:exp] + '.' + mantissa_str[exp:]
    return mantissa_str


def insert_zeros(mantissa_str, exp):
    mantissa_str = mantissa_str + '0' * exp
    return mantissa_str


def insert_sign(mantissa_str):
    return '-' + mantissa_str


def mantissa_to_str(mantissa):
    mantissa = mantissa[::-1]
    mantissa = list(map(str, mantissa))
    mantissa = pad_mantissa_blocks(mantissa)
    mantissa = ''.join(mantissa)
    return mantissa


def mantissa_is_zero(mantissa):
    return all(x == 0 for x in mantissa)


def make_zero(mantissa):
    mantissa = [0]
    return Big_float(0, mantissa, 1)


def mantissa_starts_with_zero(mantissa):
    return mantissa[0] == 0


def strip_leading_zeros(mantissa):
    while mantissa[0] == 0:
        del mantissa[0]
    return mantissa


def adjust_exp_after_strip(big_float_num, len_old_mantissa, new_mantissa):
    len_new_mantissa = len(new_mantissa)
    old_exp = big_float_num.get_exp()
    new_exp = (len_old_mantissa - len_new_mantissa) * BASE + old_exp
    return new_exp


def mantissa_ends_with_zero(mantissa):
    return mantissa[-1] == 0


def strip_trailing_zeros(mantissa):
    while mantissa[-1] == 0:
        del mantissa[-1]
    return mantissa


def pad_mantissa_blocks(mantissa):
    for i in range(1, len(mantissa)):
        if len(mantissa[i]) < BASE:
            mantissa[i] = '0' * (BASE - len(mantissa[i])) + mantissa[i]
    return mantissa


if __name__ == '__main__':
    for i in range(10):
        a = random_BF()
        print(a.exp + len(a.mantissa) * 5)
