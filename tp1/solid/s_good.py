from dataclasses import dataclass

@dataclass
class Person:
    name: str

class PersonDatabase:
    @classmethod
    def save(cls, person):
        print(f'Save the {person} to the database')

if __name__ == '__main__':
    p = Person('John Doe')
    PersonDatabase.save(p)