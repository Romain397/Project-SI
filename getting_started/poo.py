class Complex:
    # dunder
    def __init__(self, real, imag):
        self.__real = real
        self.__imag = imag

    def get_real(self):
        return self.__real
    
    def set_real(self, real):
        self.__real = real
    
    @property
    def real(self):
        return self.__real
    
    @real.setter
    def real(self, value):
        self.__real = value
        
        
class MyClass:
    i = 19

    @classmethod
    def display_i(cls):
        print(cls.i)

if __name__ == '__main__':
    c1 = Complex(12, 9)
    print(f'c getter: {c1.get_real()}')
    c1.set_real(13)
    print(f'c property: {c1.real}')
    c1.real = 14
    print(f'c property: {c1.real}')
    
    MyClass.display_i()
