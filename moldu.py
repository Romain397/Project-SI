# moldu_sorcier.py


class Moldu:
    def __init__(self, nom):
        self.nom = nom


class Sorcier(Moldu):
    def __init__(self, nom, maison):
        super().__init__(nom)
        self.maison = maison

    def lancer_un_sort(self):
        print(f"Lancer un sort par {self.nom}")
