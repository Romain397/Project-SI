class Dog:
    kind = 'canine'

    
    def __init__(self, name):
        self.tricks = []
        self.name = name
        
    def add_trick(self, trick):
        self.tricks.append(trick)
        
