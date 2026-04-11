from core import Big_float, BASE, big_float_copy, normalized
from mul import short_mul


def add(number1, number2):
    sign1 = number1.get_sign()
    sign2 = number2.get_sign()
    copy_number1 = big_float_copy(number1)
    copy_number2 = big_float_copy(number2)
    copy_number1, copy_number2 = aligned_numbers(copy_number1, copy_number2)
    if sign1 == sign2:
        answer = add_same_sign(copy_number1, copy_number2)
    else:
        answer = subtract_ordered(copy_number1, copy_number2)
    answer = normalized(answer)
    return answer


def sub(number1, number2):
    sign1 = number1.get_sign()
    sign2 = number2.get_sign()
    copy_number1 = big_float_copy(number1)
    copy_number2 = big_float_copy(number2)
    copy_number1, copy_number2 = aligned_numbers(copy_number1, copy_number2)
    if sign1 == sign2:
        answer = subtract_ordered(copy_number1, copy_number2)
    else:
        answer = add_same_sign(copy_number1, copy_number2)
    answer = normalized(answer)
    return answer


def add_same_sign(number1, number2):
    mantissa1 = number1.get_mantissa()
    mantissa2 = number2.get_mantissa()
    if len(mantissa1) >= len(mantissa2):
        new_mantissa = sum_mantissas(mantissa1, mantissa2)
    else:
        new_mantissa = sum_mantissas(mantissa2, mantissa1)
    number = Big_float(number1.get_exp(), new_mantissa, number1.get_sign())
    return number


def sum_mantissas(bigger_mantissa, smaller_mantissa):
    carry = 0
    for i in range(len(smaller_mantissa)):
        bigger_mantissa[i] += smaller_mantissa[i] + carry
        carry = 0
        if bigger_mantissa[i] >= 10**BASE:
            bigger_mantissa[i] -= 10**BASE
            carry = 1
    if carry == 1:
        if len(bigger_mantissa) == len(smaller_mantissa):
            bigger_mantissa.append(1)
        else:
            bigger_mantissa[i + 1] += 1
    return bigger_mantissa


def subtract_ordered(number1, number2):
    exp = number1.get_exp()
    sign = number1.get_sign()
    mantissa1 = number1.get_mantissa()
    mantissa2 = number2.get_mantissa()
    if bigger_or_equal_for_aligned(number1, number2):
        new_mantissa = sub_mantissas(mantissa1, mantissa2)
    else:
        new_mantissa = sub_mantissas(mantissa2, mantissa1)
        sign = sign * -1
    return Big_float(exp, new_mantissa, sign)


def sub_mantissas(mantissa1, mantissa2):
    carry = 0
    for i in range(len(mantissa2)):
        mantissa1[i] -= mantissa2[i] + carry
        carry = 0
        if mantissa1[i] < 0:
            mantissa1[i] += 10**BASE
            carry = 1
    if carry == 1:
        mantissa1 = _propagate_borrow(mantissa1, len(mantissa2))
    return mantissa1


def _propagate_borrow(mantissa, start_index):
    i = start_index
    while i < (len(mantissa) - 1) and mantissa[i] == 0:
        mantissa[i] = 99999
        i += 1
    try:
        mantissa[i] -= 1
    except IndexError:
        return [0]
    return mantissa


def aligned_numbers(number1, number2):
    exp1 = number1.get_exp()
    exp2 = number2.get_exp()
    if exp2 > exp1:
        number2 = align_a_num(number2, exp2, exp1)
    elif exp1 == exp2:
        pass
    else:
        number1 = align_a_num(number1, exp1, exp2)
    return number1, number2


def align_a_num(number, number_exp, exp_to_align):
    zeros_BASE = (number_exp - exp_to_align) // BASE
    remainder_shift = (number_exp - exp_to_align) % BASE
    number = short_mul(number, 10**(remainder_shift), -(number_exp - exp_to_align))
    mantissa = number.get_mantissa()[::-1]
    mantissa += [0] * zeros_BASE
    number.set_mantissa(mantissa[::-1])
    return number


def bigger_or_equal_for_aligned(number1, number2):
    mantissa1 = number1.get_mantissa()
    mantissa2 = number2.get_mantissa()
    if len(mantissa1) > len(mantissa2):
        return True
    elif len(mantissa1) < len(mantissa2):
        return False
    else:
        i = 0
        while True:
            i -= 1
            if -i == len(mantissa1) and mantissa1[i] == mantissa2[i]:
                return True
            if mantissa1[i] > mantissa2[i]:
                return True
            elif mantissa1[i] < mantissa2[i]:
                return False


if __name__ == '__main__':
    a = Big_float(0, [1], 1)
    b = Big_float(0, [3], 1)
    print(bigger_or_equal_for_aligned(a, b))
