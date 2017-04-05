import numpy as np
import math


def sigmoid(x):
    """Prend un réel et lui applique al fonction sigmoïde, qui l'envoie dans [0,1]

    Args:
        x (float/double): réel

    Returns:
        float: sigmoid(x)
    """
    return 1 / (1 + math.exp(-0.2 * x))


class Layer(object):

    def __init__(self, nbInput, nbOutput, prev, name="Unnamed"):
        """Layer est une couche de neurones
        Args:
            nbInput (int): nombre d'input de la couche
            nbOutput (int): nombre d'output de la couche
            prev (Layer): couche précédente
            name (str, optional): nom de la couche
        """
        self.size = nbInput * nbOutput
        self.prev = prev
        self.name = name + " (" + str(nbInput) + "x" + str(nbOutput) + ")"
        self.output = np.zeros(nbOutput)
        self.coeff = np.ones((nbOutput, nbInput))
        self.coeff[0] *= 2

    def fromDNA(dna):
        """rempli la matrice des coeffs avec l'ADN fourni

        Args:
            dna (int[]): concaténation des lignes de la matrice des coeffs

        Returns:
            void: effet de bord
        """
        pass

    def toDNA():
        """extrait l'ADN du Layer par concat des lignes de la matrice des coeffs
        Returns:
            int[]: concaténation des lignes de la matrice des coeffs
        """
        pass

    def calc(self):
        """Met à jour les ouput de __self__ en effectuant le produit matriciel input*coeff = output
        Returns:
            void: (effet de bord)
        """
        raw_coeff = np.dot(self.coeff, self.prev.output)
        for i in range(len(raw_coeff)):
            self.output[i] = sigmoid(raw_coeff[i])

    def toString(self):
        """construit une String sur plusieurs lignes permettant d'afficher explicitement le Layer

        Returns:
            String: description explicite du Layer
        """
        if(self.prev is None):
            return ("-------BEGINNING OF INPUT LAYER: ---------------\nInput Layer, no coeffs.\nNumber of inputs: " + str(len(self.output)) + "\n--------------END OF INPUT LAYER-------------")
        return ("-------BEGINNING OF LAYER: " + self.name + " ---------------\nInput \t" + str(self.prev.output) + "\nCoeffs\t" + str(self.coeff) + "\nOutput\t" + str(self.output) + "\n--------------END OF LAYER: " + self.name + "-------------")
