from core import BASE, random_BF, BF_to_str, BF_round
from subadd import sub, add
from mul import mul, short_mul
from div import div, flip_fraction 
from sq_root import sq_root
import gc

from random import randint
from decimal import Decimal, getcontext
from time import perf_counter
import os

getcontext().prec = 100000


def compare(ans, trueans, precision = 10000):
    ans = BF_to_str(ans)
    trueans = f"{trueans:.50000f}"
    if precision == 0:
        precision = len(trueans)
    point_ind = trueans.find('.')
    if point_ind != -1 and point_ind < 10000 and trueans[-1] == '0':
        i = -1
        while trueans[i] == '0':
            i -= 1
        trueans = trueans[:i]
    # if len(ans) != len(trueans) and (len(ans) < 10000 or len(trueans) < 10000): 
    #     assert ans[:min(len(trueans), len(ans))] == trueans[:min(len(trueans), len(ans))], print(ans[:min(len(trueans), len(ans))], '\n', '\n', trueans[:min(len(trueans), len(ans))])
    # else:
    if trueans == '0':
        for i in range(min(precision, len(ans))):
            if ans[i] not in ['-', '0', '.']:
                print(i)
                raise ValueError
    if ans[:precision] != trueans[:precision]: 
        for i in range(min(precision, len(trueans))):
            if i >= len(ans) or ans[i] != trueans[i]:
                print(ans[:precision], '\n', '\n', trueans[:precision])
                print(i)
                print(len(ans), len(trueans))
                raise ValueError
    


def add_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = add(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a + b
    compare(ans, trueans)
    print('.', end='', flush=True)

def sub_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = sub(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a - b
    compare(ans, trueans)
    print('.', end='', flush=True)

def mul_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = mul(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a * b
    compare(ans, trueans)
    print('.', end='', flush=True)

def short_mul_test():
    a1 = random_BF()
    b1 = randint(1, 1000)
    exp = randint(1, 1000)
    ans = short_mul(a1, b1, exp)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    b //= 10**exp
    trueans = a * b
    compare(ans, trueans, 0)
    print('.', end='', flush=True)

def div_test():
    a1 = random_BF()
    b1 = random_BF()
    ans = div(a1, b1)
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    trueans = a / b
    compare(ans, trueans)
    print('.', end='', flush=True)

def sqrt_test():
    a1 = random_BF()
    a1.set_sign(1)
    ans = sq_root(a1)
    a = Decimal(BF_to_str(a1))
    trueans = a.sqrt()
    compare(ans, trueans)
    print('.', end='', flush=True)

def sq_solve_test():
    a1 = random_BF()
    b1 = random_BF()
    c1 = random_BF()
    a = Decimal(BF_to_str(a1))
    b = Decimal(BF_to_str(b1))
    c = Decimal(BF_to_str(c1))
    d1 = mul(b1, b1, 0)
    d = b * b
    # compare(d1, d)
    d1 = sub(d1, short_mul(mul(a1, c1, 0), 4))
    d = d - 4 * a * c
    if d <= 0:
        return
    # compare(d1, d)
    if (b1.exp + len(b1.mantissa) * BASE) * 2 - a1.exp - len(a1.mantissa) * BASE - c1.exp - len(c1.mantissa) * BASE < 0:
        d1 = BF_round(d1, 2040)
        d1 = sq_root(d1)
        d = d.sqrt()
        flip_a1 = flip_fraction(a1)
        flip_a = 1 / a 
        if b1.get_sign() == -1:
            b1.set_sign(b1.get_sign() * -1)
            x11 = add(b1, d1)
            x1 = -b + d
            # compare(x11, x1)
            x11 = mul(x11, short_mul(flip_a1, 5, -1), 0)
            x1 = x1 * flip_a / 2
            compare(x11, x1)
        else:   
            b1.set_sign(b1.get_sign() * -1)
            x11 = sub(b1, d1)
            x1 = -b - d
            # compare(x11, x1)
            x11 = mul(x11, short_mul(flip_a1, 5, -1), 0)
            x1 = x1 * flip_a / 2
            compare(x11, x1)
        x22 = mul(b1, flip_a1, 0)
        x2 = -b * flip_a
        # compare(x22, x2)
        x22 = sub(x22, x11)
        x2 = x2 - x1
        compare(x22, x2)
    else:
        d1 = BF_round(d1, 2040)
        d1 = sq_root(d1)
        d = d.sqrt()
        # compare(d1, d)
        flip_a = 1 / a 
        flip_a1 = flip_fraction(a1)
        # compare(flip_a1, flip_a)
        if b1.get_sign() == -1:
            b1.set_sign(b1.get_sign() * -1)
            x11 = add(b1, d1)
            x1 = -b + d
            # compare(x11, x1)
            x11 = mul(x11, short_mul(flip_a1, 5, -1))
            x1 = x1 * flip_a / 2
            compare(x11, x1)
        else:
            b1.set_sign(b1.get_sign() * -1)
            x11 = sub(b1, d1)
            x1 = -b - d
            # compare(x11, x1)
            x11 = mul(x11, short_mul(flip_a1, 5, -1))
            x1 = x1 * flip_a / 2
            compare(x11, x1)
        flip_x11 = flip_fraction(x11)
        x22 = mul(mul(c1, flip_a1), flip_x11)
        x2 = c * flip_a / x1
        compare(x22, x2)
    print('.', end='', flush=True)
    

def benchmark(prec = 10):
    add_t = []
    sub_t = []
    mul_t = []
    div_t = []
    sq_root_t = []
    gc.disable()
    for _ in range(prec):
        a = random_BF()
        b = random_BF()
        time1 = perf_counter()
        res = add(a, b)
        time2 = perf_counter()
        add_t.append(time2 - time1)
        time1 = perf_counter()
        res = sub(a, b)
        time2 = perf_counter()
        sub_t.append(time2 - time1)
        time1 = perf_counter()
        res = mul(a, b)
        time2 = perf_counter()
        gc.collect()
        mul_t.append(time2 - time1)
        time1 = perf_counter()
        res = div(a, b)
        time2 = perf_counter()
        gc.collect()
        div_t.append(time2 - time1)
        time1 = perf_counter()
        res = sq_root(a)
        time2 = perf_counter()
        gc.collect()
        sq_root_t.append(time2 - time1)
    print(sum(add_t) / prec, 'сложение')
    print(sum(sub_t) / prec, 'вычитание')
    print(sum(mul_t) / prec, 'умножение')
    print(sum(div_t) / prec, 'деление')
    print(sum(sq_root_t) / prec, 'корень')
                

def sq_benchmark(prec = 10):
    sq_test_time = []
    for _ in range(prec):
        a1 = random_BF()
        b1 = random_BF()
        c1 = random_BF()
        gc.disable()
        time1 = perf_counter()
        d1 = mul(b1, b1, 0)
        d1 = sub(d1, short_mul(mul(a1, c1, 0), 4))
        if d1.get_sign() == -1:
            d1.set_sign(1)
            b1.set_sign(b1.get_sign() * -1)
            d1 = sq_root(d1)
            a1 = short_mul(flip_fraction(a1), 5, -1)
            x = mul(b1, a1)
            d = mul(d1, a1)
            x1 = f'{BF_to_str(x)} + {BF_to_str(d)}'
            x2 = f'{BF_to_str(x)} - {BF_to_str(d)}'
        else:
            if (b1.exp + len(b1.mantissa) * BASE) * 2 - a1.exp - len(a1.mantissa) * BASE - c1.exp - len(c1.mantissa) * BASE < 0:
                d1 = BF_round(d1, 2040)
                d1 = sq_root(d1)
                flip_a1 = flip_fraction(a1)
                if b1.get_sign() == -1:
                    b1.set_sign(b1.get_sign() * -1)
                    x11 = add(b1, d1)
                    x11 = mul(x11, short_mul(flip_a1, 5, -1), 0)
                else:   
                    b1.set_sign(b1.get_sign() * -1)
                    x11 = sub(b1, d1)
                    x11 = mul(x11, short_mul(flip_a1, 5, -1), 0)
                x22 = mul(b1, flip_a1, 0)
                x22 = sub(x22, x11)
            else:
                d1 = BF_round(d1, 2040)
                d1 = sq_root(d1)
                if b1.get_sign() == -1:
                    flip_a1 = flip_fraction(a1)
                    b1.set_sign(b1.get_sign() * -1)
                    x11 = add(b1, d1)
                    x11 = mul(x11, short_mul(flip_a1, 5, -1))
                    flip_x11 = flip_fraction(x11)
                    x22 = mul(mul(c1, flip_a1), flip_x11)
                else:
                    flip_a1 = flip_fraction(a1)
                    b1.set_sign(b1.get_sign() * -1)
                    x11 = sub(b1, d1)
                    x11 = mul(x11, short_mul(flip_a1, 5, -1))
                    flip_x11 = flip_fraction(x11)
                    x22 = mul(mul(c1, flip_a1), flip_x11)
        sq_test_time.append(perf_counter() - time1)
        gc.collect()
    print('квадратка в среднем за', sum(sq_test_time) / prec)

    # def pls_work():
    #     b = str_to_BF()
        
if __name__ == '__main__':
    benchmark()
    sq_benchmark()
    # for _ in range(10000):
    #     # add_test()
    #     # sub_test()
    #     # mul_test()
    #    # div_test()
    #     # sqrt_test()
    #     sq_solve_test()
    
        
    

