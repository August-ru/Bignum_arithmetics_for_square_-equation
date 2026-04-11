from core import Big_float, BASE
from abc import ABC, abstractmethod



class Interpretator(ABC):
    
    @abstractmethod
    def interpret(self):
        pass


class Context():

    def __init__(self):

        self.a = Big_float()
        self.b = Big_float()
        self.c = Big_float()

    def set_a(self,
              Bigfloat_number: Big_float) -> None:
        
        self.a = Bigfloat_number

    def set_b(self,
              Bigfloat_number: Big_float) -> None:
        
        self.b = Bigfloat_number

    def set_c(self,
              Bigfloat_number: Big_float) -> None:
        
        self.c = Bigfloat_number
        


class String(Interpretator):

    def __init__(self,
                 string: str,
                 context: Context):
        
        self.string = string
        self.context = context
        self.interpret()

    def interpret(self):
        coefficients = self.string.split()
        if len(coefficients) != 3:
            raise ValueError("Неверное число коэффицентов")
        a = Coefficient(coefficients[0]).interpret()
        b = Coefficient(coefficients[1]).interpret()
        c = Coefficient(coefficients[2]).interpret()
        self.context.set_a(a)
        self.context.set_b(b)
        self.context.set_c(c)

        
class Coefficient(Interpretator):

    def __init__(self,
                 coefficient: str):
        
        self.coefficient = coefficient


    def interpret(self):
        number = Big_float()
        number.set_exp(Exp(self.coefficient).interpret())
        number.set_sign(Sign(self.coefficient).interpret())
        number.set_mantissa(Mantissa(self.coefficient).interpret())
        return number

class Exp(Interpretator):

    def __init__(self,
                 coefficient: str):
        
        self.coefficient = coefficient

    def interpret(self):
        
        index_of_point = self.coefficient.find('.')
        if index_of_point != -1:
            exp = index_of_point - len(self.coefficient) + 1
        else:
            exp = 0
        return exp
    
class Mantissa(Interpretator):

    def __init__(self,
                 coefficient: str):
        coefficient = coefficient.replace('-', '')
        coefficient = coefficient.replace('.', '')
        self.coefficient = coefficient

    def interpret(self):
        
        mantissa = []
        n = len(self.coefficient)
        for i in range(n, 0, -BASE):
            start = max(0, i - BASE)
            chunk = Chunk(self.coefficient[start:i]).interpret()
            mantissa.append(chunk)
        return mantissa
    
class Sign(Interpretator):

    def __init__(self,
                 coefficient: str):
        
        self.coefficient = coefficient

    def interpret(self) -> int:
        if self.coefficient[0] == '-':
            return -1
        else:
            return 1
        
class Chunk(Interpretator):

    def __init__(self,
                chunk: str):
        
        self.chunk = chunk

    def interpret(self):
        try:
            chunk = int(self.chunk)
            return chunk
        except:
            raise ValueError("Строка не может быть переведена в коэффиценты")


if __name__ == '__main__':
    s = '56789470597420000 0.679843 435806.98'
       

    
        
        