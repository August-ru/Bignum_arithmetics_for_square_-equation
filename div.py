from mul import mul
from core import BASE, BF_round, BF_to_str, random_BF
from subadd import sub
from str_to_big_float import str_to_BF, int_to_BF


def div(num1, num2):
    approx = initial_reciprocal_approx(num2)
    reciprocal = newton_algorithm(num2, approx)
    result = mul(num1, reciprocal)
    return result


def flip_fraction(num):
    approx = initial_reciprocal_approx(num)
    reciprocal = newton_algorithm(num, approx)
    return reciprocal


def initial_reciprocal_approx(num):
    mantissa = num.get_mantissa()
    sign = num.get_sign()
    if len(mantissa) > 3:
        return _approx_large_mantissa(mantissa, sign, num.get_exp())
    else:
        return _approx_small_mantissa(mantissa, sign, num.get_exp())


def _approx_large_mantissa(mantissa, sign, num_exp):
    mantissa_len = len(mantissa)
    high_block = mantissa[-1] * 10**(BASE * (mantissa_len - 2))
    mid_block = mantissa[-2] * 10**(BASE * (mantissa_len - 3))
    low_block = mantissa[-3] * 10**(BASE * (mantissa_len - 4))
    approx = 10**(BASE * mantissa_len + 1) // (high_block + mid_block + low_block)
    approx = int_to_BF(approx)
    new_exp = approx.get_exp() - BASE * (mantissa_len + 1) - num_exp - 1
    approx.set_exp(new_exp)
    approx.set_sign(sign)
    return approx


def _approx_small_mantissa(mantissa, sign, num_exp):
    mantissa_len = len(mantissa)
    if mantissa_len == 2:
        approx_value = 1 / (mantissa[-1] * 10**BASE + mantissa[-2])
        approx = str_to_BF(f"{approx_value:.30f}")
    else:
        approx_value = 1 / mantissa[-1]
        approx = str_to_BF(f"{approx_value:.30f}")
    new_exp = approx.get_exp() - num_exp 
    approx.set_exp(new_exp)
    approx.set_sign(sign)
    return approx


def newton_algorithm(num, approx, precision=11):
    accuracy = 2
    for _ in range(precision):
        accuracy *= 2
        a = sub(str_to_BF('2'), mul(BF_round(num, accuracy + 10), approx, accuracy + 10))
        approx = mul(approx, a, accuracy + 20)
    return approx


if __name__ == '__main__':
    a = flip_fraction(str_to_BF('0.318309886'))
    print(BF_to_str(a))
