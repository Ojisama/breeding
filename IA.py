# coding: utf-8

def directionAuto(input):
    un = (input[0] == 1)
    deux = (input[1] == 1)
    if deux:
        return gauche(input)
    elif un:
        return droite(input)
    else:
        return toutDroit(input)
    

def gauche(input):
    gauche = (input[4] == 1)
    toutDroit = (input[5] == 1)
    droite = (input[6] == 1)
    if not gauche:
        return 0
    elif (gauche and not droite) or (gauche and toutDroit):
        return 2
    elif (gauche and not toutDroit) or (gauche and droite):
        return 1


def droite(input):
    gauche = (input[4] == 1)
    toutDroit = (input[5] == 1)
    droite = (input[6] == 1)
    if not droite:
        return 2
    elif (droite and not gauche) or (droite and toutDroit):
        return 0
    elif (droite and not toutDroit) or (droite and gauche):
        return 1  

    
def toutDroit(input):
    gauche = (input[4] == 1)
    toutDroit = (input[5] == 1)
    droite = (input[6] == 1)
    trois = (input[2] == 1)
    quatre = (input[3] == 1)
    if not toutDroit:
        return 1
    elif (toutDroit and gauche):
        return 2
    elif (toutDroit and droite):
        return 0
