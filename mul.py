from core import Big_float, BASE, normalized, random_BF, BF_round
from str_to_big_float import str_to_BF
import cmath, math, copy
from functools import lru_cache
from itertools import chain
import operator

BLOCK_SIZE = 10 ** BASE


def calculate_fft_cache(max_log2):
    cache = []
    for s in range(max_log2 + 1):
        cache.append([])
        for q in range(2**s):
            angle = -2 * cmath.pi * q / 2**s
            cache[s].append(cmath.rect(1.0, angle))
    return cache


def calculate_ifft_cache(cache):
    new_cache = copy.deepcopy(cache)
    for i in range(len(cache)):
        for j in range(len(cache[i])):
            new_cache[i][j] = new_cache[i][j].conjugate()
    return new_cache

FFT_CACHE = calculate_fft_cache(16)
IFFT_CACHE = calculate_ifft_cache(FFT_CACHE)


def short_mul(number, integ, exp_delta=0):
    mantissa = number.get_mantissa()
    abs_integ = abs(integ)
    mantissa = [block * abs_integ for block in mantissa]
    mantissa = propagate_carries(mantissa)
    sign = number.get_sign() * (abs_integ // integ)
    return Big_float(number.get_exp() + exp_delta, mantissa, sign)


def mul(number1, number2, precision=2040):
    new_exp = number1.get_exp() + number2.get_exp()
    new_sign = number1.get_sign() * number2.get_sign()
    mantissa1, mantissa2 = number1.get_mantissa(), number2.get_mantissa()
    new_mantissa = mantissa_mul(mantissa1, mantissa2)
    result = Big_float(new_exp, new_mantissa, new_sign)
    result = normalized(result)
    if precision != 0:
        result = BF_round(result, precision)
    return result


def mantissa_mul(mantissa1, mantissa2):
    mantissa1, mantissa2 = pad_to_power_of_two(mantissa1, mantissa2)
    spectrum1, spectrum2 = RFFT(mantissa1, mantissa2)
    product_spectrum = pointwise_multiply(spectrum1, spectrum2)
    new_mantissa = inverse_fft_to_mantissa(product_spectrum)
    return new_mantissa


def pad_to_power_of_two(mantissa1, mantissa2):
    sum_len = len(mantissa1) + len(mantissa2) - 1
    needed_len = calc_needed_len(sum_len)
    mantissa1 += [0] * (needed_len - len(mantissa1))
    mantissa2 += [0] * (needed_len - len(mantissa2))
    return mantissa1, mantissa2


def complex_packing(mantissa1, mantissa2):
    return list(map(complex, mantissa1, mantissa2))


def complex_unpacking(points):
    return list(chain.from_iterable(
        (round(p.real), round(p.imag)) for p in points
    ))


def calc_needed_len(sum_len):
    needed_len = 1 << math.ceil(math.log2(sum_len))
    if needed_len == 1:
        needed_len += 1
    return needed_len


def RFFT(mantissa1, mantissa2):
    coef = complex_packing(mantissa1, mantissa2)
    coef = bit_reverse(coef)
    n = len(coef)
    fft_cache = FFT_CACHE
    cache_ind = 0
    for s in range(1, int(math.log2(n) + 0.5) + 1):
        cache_ind += 1
        butterfly_len = 1 << s
        half = butterfly_len >> 1
        cache_level = fft_cache[cache_ind]
        for i in range(0, n, butterfly_len):
            for j in range(half):
                idx = i + j
                omega = cache_level[j]
                t = omega * coef[idx + half]
                coef[idx + half] = coef[idx] - t
                coef[idx] += t
    fft1, fft2 = spectres_forming(coef)
    return fft1, fft2


def IRFFT(points):
    points = spectre_unforming(points)
    points = bit_reverse(points)
    n = len(points)
    ifft_cache = IFFT_CACHE
    cache_ind = 0
    for s in range(1, int(math.log2(n) + 0.5) + 1):
        cache_ind += 1
        butterfly_len = 1 << s
        half = butterfly_len >> 1
        cache_level = ifft_cache[cache_ind]
        for i in range(0, n, butterfly_len):
            for j in range(half):
                idx = i + j
                omega = cache_level[j]
                t = omega * points[idx + half]
                points[idx + half] = points[idx] - t
                points[idx] += t
    inv_n = 1.0 / n
    points = [x * inv_n for x in points]
    points = complex_unpacking(points)
    return points


def spectres_forming(points):
    n = len(points)
    half_n = n >> 1
    spectre1 = [0] * (half_n + 1)
    spectre2 = [0] * (half_n + 1)
    for k in range(half_n + 1):
        j = (n - k) % n
        conj_point = points[j].conjugate()
        spectre1[k] = (points[k] + conj_point) * 0.5
        spectre2[k] = (points[k] - conj_point) * (-0.5j)
    return spectre1, spectre2


def spectre_unforming(spectre):
    n = len(spectre) - 1
    fft = [0] * n
    fft[0] = complex((spectre[0] + spectre[-1]) / 2, (spectre[0] - spectre[-1]) / 2)
    cache_ind = int(math.log2((len(spectre) - 1) * 2) + 0.5)
    ifft_level = IFFT_CACHE[cache_ind]
    for k in range(1, n):
        omega = ifft_level[k]
        a = spectre[k]
        b = spectre[n - k].conjugate()
        fft[k] = 0.5 * ((a + b) + 1j * omega * (a - b))
    return fft


def bit_reverse(arr):
    n = len(arr)
    rev = calc_ind(n)
    for i in range(n):
        j = rev[i]
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    return arr

@lru_cache(maxsize=500)
def calc_ind(n):
    bits = n.bit_length() - 1
    rev = [0] * n
    for i in range(1, n):
        rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (bits - 1))
    return rev


def inverse_fft_to_mantissa(points):
    new_mantissa = IRFFT(points)
    result = propagate_carries(new_mantissa)
    return result


def propagate_carries(mantissa):
    carry = 0
    for i in range(len(mantissa)):
        value = mantissa[i] + carry
        carry, mantissa[i] = divmod(value, BLOCK_SIZE)
    if carry != 0:
        mantissa.append(carry % BLOCK_SIZE)
    return mantissa


def pointwise_multiply(spectrum1, spectrum2):
    return list(map(operator.mul, spectrum1, spectrum2))


if __name__ == '__main__':
    a = random_BF()
    b = str_to_BF('3')
    print(a.exp)
    print(mul(a, b).exp)
