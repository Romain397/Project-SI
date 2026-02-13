# Classe Moldu
class Moldu:
    def __init__(self, nom):
        self.nom = nom


# Classe Sorcier qui hérite de Moldu
class Sorcier(Moldu):
    def __init__(self, nom, maison):
        super().__init__(nom)
        self.maison = maison

    def lancer_un_sort(self):
        print(f"Lancer un sort par {self.nom}")


# Création des instances
harry = Sorcier("Harry", "Gryffondor")
jean = Moldu("Jean")

# Test
harry.lancer_un_sort()
