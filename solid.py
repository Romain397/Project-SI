# solid.py

from abc import ABC, abstractmethod

# =====================
# S - Single Responsibility
# =====================


class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name})"


class PersonDB:
    def save(self, person):
        print(f"Save {person} to database")


# =====================
# O - Open Closed
# =====================


class Storage(ABC):
    @abstractmethod
    def save(self, person):
        pass


class DatabaseStorage(Storage):
    def save(self, person):
        print(f"Save {person} to database")


class JSONStorage(Storage):
    def save(self, person):
        print(f"Save {person} to JSON file")


# =====================
# L - Liskov Substitution
# =====================


class Notification(ABC):
    @abstractmethod
    def notify(self, message, contact):
        pass


class Email(Notification):
    def notify(self, message, contact):
        print(f"Send {message} to email {contact}")


class SMS(Notification):
    def notify(self, message, contact):
        print(f"Send {message} to phone {contact}")


# =====================
# I - Interface Segregation
# =====================


class Drivable(ABC):
    @abstractmethod
    def go(self):
        pass


class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass


class Car(Drivable):
    def go(self):
        print("Driving")


class Aircraft(Drivable, Flyable):
    def go(self):
        print("Taxiing")

    def fly(self):
        print("Flying")


# =====================
# D - Dependency Inversion
# =====================


class Converter(ABC):
    @abstractmethod
    def convert(self, from_currency, to_currency, amount):
        pass


class FXConverter(Converter):
    def convert(self, from_currency, to_currency, amount):
        result = amount * 1.2
        print(f"{amount} {from_currency} = {result} {to_currency}")
        return result


class App:
    def __init__(self, converter: Converter):
        self.converter = converter

    def start(self):
        self.converter.convert("EUR", "USD", 100)
