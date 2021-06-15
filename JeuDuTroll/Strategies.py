import random
import Solveur as simplex

def StrategieAleatoire(n):
    if n//2 > 1 : 
        rand = random.randint(1,n//2)
    else :
        rand = 1
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
    if nbPierresCourant > 1 :
        rand = random.random()
        matrice = []
        for i in range(nbPierresCourant-1) :
            col = []
            for j in range(nbPierresCourantAdversaire-1) :
                col.append(float("inf"))
            matrice.append(col)
        simplex.MatriceGains(nbPierresCourant-1,nbPierresCourantAdversaire-1,positionTroll,nbCases,matrice)
        s = simplex.SimplexGainsMatrice(len(matrice),len(matrice[0]),matrice)
        probabilitesStrategieMixte = s.x
        print(probabilitesStrategieMixte)
        acc = 1
        i = nbPierresCourant-1
        while acc > rand and i > 1:
            acc -= probabilitesStrategieMixte[i]
            i-=1
        return i
    else :
        return 1