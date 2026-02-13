class Person:

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'Person(name={self.name})'
    
class PersonStorage:
        
    def save_to_database(self, person):
        print(f'Save the {person} to database')
        
    def save_to_json(self, person):
        print(f'Save the {person} to a JSON file')

if __name__ == '__main__':
    person = Person('John Doe')
    storage = PersonStorage()
    storage.save_to_database(person)