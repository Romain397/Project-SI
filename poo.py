class Complex:
    def init(self, real, imag):
        self.real = real
        self.imag = imag

    def str(self):
        return f"{self.real} + {self.imag}i"

    def add(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        return NotImplemented

    def mul(self, other):
        if isinstance(other, Complex):
            real_part = self.real * other.real - self.imag * other.imag
            imag_part = self.real * other.imag + self.imag * other.real
            return Complex(real_part, imag_part)
        return NotImplemented
