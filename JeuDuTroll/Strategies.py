# module qui comporte toutes les fonctions de strategie
import random
import Solveur as simplex

def StrategieTest() : # strategir non rationnelle qui consiste a toujours lancer une pierre.
    return 1

def StrategieAleatoire(n): # strategie aleatoire. Il n'est pas rationnel de jouer un coup superieur a la moitie de ses pierres, c est donc aleatoire entre 0 et n//2.
    if n//2 > 1 : 
        rand = random.randint(1,n//2)
    else :
        rand = random.randint(1,n)
    print ("Coup joue : ", rand)
    return rand


def StrategiePrudentePure(nbPierresTotal,nbCases,nbPierresCourant) : # Le troll doit bouger de NbCase //2 au maximum afin d'aller dans le chateau d'un joueur.
    distanceParcoursTroll = nbCases//2 # L'idee de cette strategie est d envoyer le minimum de pierres, tout en maximisant la frequence a laquelle le troll se deplace.
    if nbPierresTotal//distanceParcoursTroll <= nbPierresCourant :
        return nbPierresTotal//distanceParcoursTroll
    else :
        return nbPierresCourant

def Strategie1(nbPierresTotal,nbCases,nbPierresCourant,nbPierresCourantAdversaire,positionTroll,joueur) : # Dans certains cas, envoyer une pierre seulement est pertinent. On choisit donc la strategie "envoyer 1" ou la strategie ci-dessus en fonction des cas.
    if nbPierresCourant <= nbCases-1 and nbPierresCourant > nbPierresCourantAdversaire and ( (positionTroll >= (nbCases//2) + 1 and joueur == 1) or (positionTroll <= (nbCases//2) + 1 and joueur == 2) ):
        return StrategieTest()
    else :
        return StrategiePrudentePure(nbPierresTotal,nbCases,nbPierresCourant)


def StrategieDerniereChance(nbCases,nbPierresCourant,nbPierresCourantAdversaire, positionTroll,joueur): # Si le troll est proche du chateau d'un joueur, il peut être pertinent de l'empêcher de le faire avancer de nouveau en envoyant le nombre de pierres que l'adversaire peut envoyer.
    if ( (positionTroll == 2 and joueur == 1) or (positionTroll ==  nbCases-1 and joueur == 2) ) and nbPierresCourant >= nbPierresCourantAdversaire :
        return nbPierresCourantAdversaire
    else :
        StrategieTest()


# Les strategies listees ci-dessus peuvent être contrees si le joueur adverse connait la fonction que l'on choisit de lancer pour le jeu.

# On va donc essayer de creer une strategie mixte qui pourrait faire gagner dans la plupart des cas, par l'intermediaire de simplex successifs de matrices de gains associées a la situation de jeu courante.
def StrategieMixteOptimale(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) :
    #Calcul de la matrice de gains
    if nbPierresCourant > 1 : # Si il ne reste qu'une seule pierre, on peut retourner 1 directement.
        rand = random.random() # tirage d'un nombre aleatoire.
        matrice = []
        for i in range(nbPierresCourant-1) :
            col = []
            for j in range(nbPierresCourantAdversaire-1) :
                col.append(float("inf"))
            matrice.append(col) # creation d'une matrice qui va stocker les gains.
        simplex.MatriceGains(nbPierresCourant-1,nbPierresCourantAdversaire-1,positionTroll,nbCases,matrice) # calcul de la matrice de gains en fonction du nombre de pierres lancees
        s = simplex.SimplexGainsMatrice(nbPierresCourant-1,nbPierresCourantAdversaire-1,matrice) # simplex de la matrice du sous-jeu afin d'obtenir le gain et la distribution de probabilites des coups a jouer
        probabilitesStrategieMixte = s.x # distribution de probabilites des coups possibles, avec x[0] le cas ou le joueur lance toutes ses pierres et x[nbPierresCourant-1] le cas ou le joueur ne lance qu'une seule pierre.
        print(probabilitesStrategieMixte) # affichage de la distribution de probabilites, a commenter / decommenter au besoin.
        acc = 1
        i = nbPierresCourant -1
        while acc > rand and i > 1:
            acc -= probabilitesStrategieMixte[nbPierresCourant -i]
            i-=1
        return i # On cherche dans la distribution de probabilites le coup i qui est associe au nombre de l'on a tire.
    else :
        return 1
