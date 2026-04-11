from core import BASE, BF_to_str
from subadd import sub, add
from mul import mul, short_mul
from div import flip_fraction, div
from sq_root import sq_root
import interpretator

NO_ROOTS = -3
INFINITLY_MANY_ROOTS = -2
LINEAR_ROOT = -1
ONE_SQ_ROOT = 0
REAL_SQ_ROOTS = 1
COMPLEX_SQ_ROOTS = 2

class Answer:
    def __init__(self, message, **kwargs):
        self.message = message
        if message == REAL_SQ_ROOTS or message == COMPLEX_SQ_ROOTS:
            self.x1 = kwargs['x1']
            self.x2 = kwargs['x2']
        elif message == ONE_SQ_ROOT or message == LINEAR_ROOT:
            self.x = kwargs['x']
        else:
            pass
    
    def get_message(self):
        return self.message

    def get_x(self):
        return self.x
    
    def get_x1(self):
        return self.x1
    
    def get_x2(self):
        return self.x2
        



def get_data():
    context = interpretator.Context()
    interpretator.String(input(), context)
    a = context.a
    b = context.b
    c = context.c
    return a, b, c


def solve(data):
    a, b, c = data
    if number_is_zero(a):
        return linear_solve(b, c)
    else:
        return square_solve(a, b, c)
    

def linear_solve(b, c):
    if number_is_zero(b):
        if number_is_zero(c):
            return Answer(INFINITLY_MANY_ROOTS)
        else:
            return Answer(NO_ROOTS)
    flip_sign(c)
    x = div(c, b)
    return Answer(LINEAR_ROOT, x=x)
      

def square_solve(a, b, c):
    discriminant = calc_discriminant(a, b, c)
    if is_negative(discriminant):
        return complex_roots(a, b, discriminant)
    elif number_is_zero(discriminant):
        return solve_one_root(a, b)
    else:
        if is_subtraction_stable(b, a, c):
            return solve_via_vieta_sub(a, b, discriminant)
        else:
            return solve_via_vieta_div(a, b, c, discriminant)


def calc_discriminant(a, b, c):
    discriminant = mul(b, b, 0)
    discriminant = sub(discriminant, short_mul(mul(a, c, 0), 4))
    return discriminant


def number_is_zero(number):
    return number.mantissa == [0]

def complex_roots(a, b, discriminant):
    flip_sign(discriminant)
    flip_sign(b)
    discriminant = sq_root(discriminant)
    a = short_mul(flip_fraction(a), 5, -1)
    x = mul(b, a)
    d = mul(discriminant, a)
    x1 = f'{BF_to_str(x)} + i{BF_to_str(d)}'
    x2 = f'{BF_to_str(x)} - i{BF_to_str(d)}'
    return Answer(COMPLEX_SQ_ROOTS, x1=x1, x2=x2)


def is_subtraction_stable(b, a, c):
    b_magnitude = b.get_exp() + len(b.get_mantissa()) * BASE
    ac_magnitude = a.get_exp() + len(a.get_mantissa()) * BASE + c.get_exp() + len(c.get_mantissa()) * BASE
    return b_magnitude * 2 - ac_magnitude < 0


def solve_via_vieta_sub(a, b, discriminant):
    discriminant = sq_root(discriminant)
    flip_a = flip_fraction(a)
    x1 = calc_x1(a, b, discriminant, 0)
    x2 = mul(b, flip_a, 0)
    x2 = sub(x2, x1)
    return Answer(REAL_SQ_ROOTS, x1=x1, x2=x2)


def solve_one_root(a, b):
    flip_sign(b)
    flip_a = flip_fraction(a)
    x = mul(b, short_mul(flip_a, 5, -1))
    return Answer(ONE_SQ_ROOT, x=x)


def solve_via_vieta_div(a, b, c, discriminant):
    discriminant = sq_root(discriminant)
    flip_a = flip_fraction(a)
    x1 = calc_x1(a, b, discriminant)
    flip_x1 = flip_fraction(x1)
    x2 = mul(mul(c, flip_a), flip_x1)
    return Answer(REAL_SQ_ROOTS, x1=x1, x2=x2)


def is_negative(number):
    return number.get_sign() == -1


def flip_sign(number):
    number.set_sign(number.get_sign() * -1)


def calc_x1(a, b, discriminant, precision=2040):
    flip_a = flip_fraction(a)
    flip_sign(b)
    if b.get_sign() == 1:
        x1 = add(b, discriminant)
    else:
        x1 = sub(b, discriminant)
    x1 = mul(x1, short_mul(flip_a, 5, -1), precision)
    return x1


def output(res):
    message = res.get_message()
    if message == REAL_SQ_ROOTS:
        out_real_sq_roots(res)
    elif message == COMPLEX_SQ_ROOTS:
        out_complex_sq_roots(res)
    elif message == ONE_SQ_ROOT or message == LINEAR_ROOT:
        out_a_root(res)
    elif message == NO_ROOTS:
        out_message_not_roots()
    elif message == INFINITLY_MANY_ROOTS:
        out_message_infinite_roots()

def out_real_sq_roots(res):
    x1 = res.get_x1()
    x2 = res.get_x2()
    x1 = BF_to_str(x1)
    x2 = BF_to_str(x2)
    print(f'x1 = {x1}')
    print(f'x2 = {x2}')

def out_complex_sq_roots(res):
    x1 = res.get_x1()
    x2 = res.get_x2()
    print(f'x1 = {x1}')
    print(f'x2 = {x2}')

def out_a_root(res):
    x = res.get_x()
    x = BF_to_str(x)
    print(f'x = {x}')

def out_message_not_roots():
    print('Уравнение корней не имеет')

def out_message_infinite_roots():
    print('Уравнение имеет бесконечное число корней')


data = get_data()
res = solve(data)
output(res)
