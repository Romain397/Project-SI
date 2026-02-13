from abc import ABC, abstractmethod

class Person:

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'Person(name={self.name})'
    
class PersonStorage(ABC):
    
    @abstractmethod
    def save(self, person):
        ...

class PersonStorageDB(PersonStorage):

    def save(self, person):
        print(f'Save the {person} to database')

class PersonStorageJson(PersonStorage):

    def save(self, person):
        print(f'Save the {person} to a JSON file')

class PersonStorageCSV(PersonStorage):

    def save(self, person):
        print(f'Save the {person} to a CSV file')


if __name__ == '__main__':
    person = Person('John Doe')
    storage = PersonStorageCSV()
    storage.save(person)

    