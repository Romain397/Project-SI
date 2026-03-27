from abc import ABC, abstractmethod

class Converter(ABC):
    
    @abstractmethod
    def convert(self, from_currency, to_currency, amount):
        pass

class FXConverter(Converter):

    def convert(self, from_currency, to_currency, amount):
        print(f'{amount} {from_currency} = {amount * 1.2},{to_currency}')
        return amount * 1.2
    
class BCConverter(Converter):

    def convert(self, from_currency, to_currency, amount):
        print(f'{amount} {from_currency} = {amount * 1.2},{to_currency}')
        return amount * 10

class App:
    
    def __init__(self, converter:Converter):
        self.__converter = converter

    def start(self):
        self.__converter.convert('EUR', 'USD', 100)

if __name__ == '__main__':
    app = App(BCConverter())
    app.start()

