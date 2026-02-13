class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name})"


class PersonDB:
    def save(self, person):
        print(f"Save {person} to database")
