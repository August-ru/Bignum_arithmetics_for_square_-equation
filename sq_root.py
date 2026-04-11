from core import BASE, Big_float, big_float_copy, BF_round, BF_to_str
from mul import mul, short_mul
from subadd import sub
from str_to_big_float import str_to_BF


ROOT_OF_10 = Big_float(-18, [79331, 1683, 27766, 3162], 1)
constant_for_newton = str_to_BF('3')


def sq_root(number):
    number = big_float_copy(number)
    reciprocal_approx = initial_approximation(number)
    reciprocal_sqrt = newton_algorithm(number, reciprocal_approx)
    result = mul(number, reciprocal_sqrt, 2040)
    return result


def initial_approximation(number):
    mantissa = number.get_mantissa()
    high_block = mantissa[-1]
    low_block = mantissa[-2] if len(mantissa) > 1 else 0
    approx = _calc_initial_value(high_block, low_block)
    new_exp = _calc_reciprocal_sqrt_exponent(number, approx, high_block, low_block)
    approx.set_exp(new_exp)
    approx.set_sign(1)
    if number.get_exp() % 2 == 1:
        approx = mul(approx, ROOT_OF_10)
    return approx


def _calc_initial_value(high_block, low_block):
    if low_block != 0:
        approx_value = 1 / ((high_block * 10**BASE + low_block) ** 0.5)
        approx = str_to_BF(f'{approx_value:.50f}')
    else:
        approx_value = 1 / (high_block ** 0.5)
        approx = str_to_BF(f'{approx_value:.15f}')
    return approx


def _calc_reciprocal_sqrt_exponent(number, approx, high_block, low_block):
    mantissa = number.get_mantissa()
    total_digits = number.get_exp() + BASE * len(mantissa)
    if low_block != 0:
        base_exp = approx.get_exp() - (number.get_exp() + BASE * (len(mantissa) - 2)) // 2
        if total_digits % 2 != 0:
            base_exp -= 1
    else:
        base_exp = approx.get_exp() - number.get_exp() // 2
    return base_exp


def newton_algorithm(number, approx, precision=11):
    accuracy = 2
    for _ in range(precision):
        accuracy *= 2
        num = BF_round(number, accuracy + 10)
        yn = mul(mul(approx, approx, accuracy + 20), num, accuracy + 10)
        yn = short_mul(sub(constant_for_newton, yn), 5, -1)
        approx = mul(approx, yn, accuracy + 10)
    return approx


if __name__ == '__main__':
    a = str_to_BF('0.03')
    a = sq_root(a)
    print(BF_to_str(a))