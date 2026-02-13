# vaisseaux.py


class Vaisseau:
    def __init__(self, nom, couleur, vitesse_nominale, duree_acceleration):
        self.nom = nom
        self.couleur = couleur
        self.vitesse_nominale = vitesse_nominale
        self.duree_acceleration = duree_acceleration
        self.position = 0
        self.vitesse_actuelle = 0
        self.tick = 0

    def avancer(self):
        self.tick += 1

        if self.tick <= self.duree_acceleration:
            self.vitesse_actuelle = (
                self.vitesse_nominale / self.duree_acceleration
            ) * self.tick
        else:
            self.vitesse_actuelle = self.vitesse_nominale

        self.position += self.vitesse_actuelle

    def afficher_position(self):
        print(f"{self.nom} position : {round(self.position, 2)}")


class Circuit:
    def __init__(self, distance_tour, nb_tours):
        self.distance_totale = distance_tour * nb_tours
