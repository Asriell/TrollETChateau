import random
import Solveur as simplex

def StrategieAleatoire(n):
    rand = random.randint(1,n//2)
    print ("Coup joue : ", rand)
    return rand


def Strategie1(nbPierresTotal,nbCases,nbPierresCourant,nbPierresCourantAdversaire,positionTroll,joueur) :
    if nbPierresCourant <= nbCases-1 and nbPierresCourant > nbPierresCourantAdversaire and ( (positionTroll >= (nbCases//2) + 1 and joueur == 1) or (positionTroll <= (nbCases//2) + 1 and joueur == 2) ):
        return StrategieTest()
    else :
        return StrategiePrudente(nbPierresTotal,nbCases,nbPierresCourant)


def StrategieDerniereChance(nbCases,nbPierresCourant,nbPierresCourantAdversaire, positionTroll,joueur):
    if ( (positionTroll == 2 and joueur == 1) or (positionTroll ==  nbCases-1 and joueur == 2) ) and nbPierresCourant >= nbPierresCourantAdversaire :
        return nbPierresCourantAdversaire
    else :
        StrategieTest()

def StrategieTest() :
    return 1


#def StrategiePrudentePure(nbPierresTotal,nbCases,nbPierresCourant) :
#    distanceParcoursTroll = nbCases//2
#    if nbPierresTotal//distanceParcoursTroll <= nbPierresCourant :
#        return nbPierresTotal//distanceParcoursTroll
#    else :
#        return nbPierresCourant

def StrategieMixteOptimale(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) :
    #Calcul de la matrice de gains
    rand = random.random()
    matrice = []
    for i in range(nbPierresCourant) :
        col = []
        for j in range(nbPierresCourantAdversaire) :
            col.append(float("inf"))
        matrice.append(col)
    simplex.MatriceGains(nbPierresCourant,nbPierresCourantAdversaire,positionTroll,nbCases,matrice)
    s = simplex.SimplexGainsMatrice(len(matrice),len(matrice[0]),matrice)
    probabilitesStrategieMixte = s.x
    acc = 0
    i = 0
    while acc <= rand :
        acc += probabilitesStrategieMixte[i]
        i+=1
    return i