# module qui comporte toutes les fonctions de strategie
import random
import numpy as np
import Solveur as simplex


def StrategieTest() : # strategie non rationnelle qui consiste a toujours lancer une pierre. Il s'agit d'une strategie de debogage.
    return 1

def StrategieAleatoire(n): # strategie aleatoire. Il n'est pas rationnel de jouer un coup superieur a la moitie de ses pierres, c est donc aleatoire entre 0 et n//2.
    if n//2 > 1 : 
        rand = random.randint(1,n//2)
    else :
        rand = random.randint(1,n)
    print ("Coup joue : ", rand)
    return rand


def StrategieAgressive(nbPierresTotal,nbCases,nbPierresCourant) : # Le troll doit bouger de NbCase //2 au maximum afin d'aller dans le chateau d'un joueur.
    distanceParcoursTroll = nbCases//2 # L'idee de cette strategie est d envoyer le maximum de pierres, tout en maximisant la frequence a laquelle le troll se deplace en faveur du joueur.
    if nbPierresTotal//distanceParcoursTroll <= nbPierresCourant :
        return nbPierresTotal//distanceParcoursTroll
    else :
        return nbPierresCourant

def Strategie1(nbPierresTotal,nbCases,nbPierresCourant,nbPierresCourantAdversaire,positionTroll,joueur) : # Dans certains cas, envoyer une pierre seulement est pertinent. On choisit donc la strategie "envoyer 1" ou la strategie ci-dessus en fonction des cas.
    if nbPierresCourant <= nbCases-1 and nbPierresCourant > nbPierresCourantAdversaire and ( (positionTroll >= (nbCases//2) + 1 and joueur == 1) or (positionTroll <= (nbCases//2) + 1 and joueur == 2) ):
        return StrategieTest()
    else :
        return StrategieAgressive(nbPierresTotal,nbCases,nbPierresCourant)


def StrategieDerniereChance(nbCases,nbPierresCourant,nbPierresCourantAdversaire, positionTroll,joueur): # Si le troll est proche du chateau d'un joueur, il peut être pertinent de l'empêcher de le faire avancer de nouveau en envoyant le nombre de pierres que l'adversaire peut envoyer.
    if ( (positionTroll == 2 and joueur == 1) or (positionTroll ==  nbCases-1 and joueur == 2) ) and nbPierresCourant >= nbPierresCourantAdversaire :
        return nbPierresCourantAdversaire
    else :
        StrategieTest()


# Les strategies listees ci-dessus peuvent être contrees si le joueur adverse connait la fonction que l'on choisit de lancer pour le jeu.

# On va donc essayer de creer une strategie mixte qui pourrait faire gagner dans la plupart des cas, par l'intermediaire de simplex successifs de matrices de gains associees a la situation de jeu courante.
def StrategiePrudente(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) :
    #Calcul de la matrice de gains
    if nbPierresCourant > 1 : # Si il ne reste qu'une seule pierre, on peut retourner 1 directement.
        matrice = []
        for i in range(nbPierresCourant) :
            col = []
            for j in range(nbPierresCourantAdversaire) :
                col.append(float("inf"))
            matrice.append(col) # creation d'une matrice qui va stocker les gains.
        simplex.MatriceGains(nbPierresCourant,nbPierresCourantAdversaire,positionTroll,nbCases,matrice) # calcul de la matrice de gains en fonction du nombre de pierres lancees
        s = simplex.solve(matrice) # simplex de la matrice du sous-jeu afin d'obtenir le gain et la distribution de probabilites des coups a jouer
        probabilitesStrategieMixte = s.x # distribution de probabilites des coups possibles, avec x[0] le cas ou le joueur lance toutes ses pierres et x[nbPierresCourant-1] le cas ou le joueur ne lance qu'une seule pierre.
        print(probabilitesStrategieMixte) # affichage de la distribution de probabilites, a commenter / decommenter au besoin.
        probasSansGain = np.delete(probabilitesStrategieMixte,len(probabilitesStrategieMixte)-1) #retrait de la valeur de gain, pour seulement avoir les différentes probabilites
        probasSansGain = list(map(lambda x: abs(x),probasSansGain))
        i = np.random.choice(len(probasSansGain),p=probasSansGain) #selection d'un indice selon les probabilites
        return nbPierresCourant - i #pierres du joueur - pierresRestantes apres lancer = nombre de pierres lancees
    else :
        return 1



def StrategiePrudenteJ2(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) : # equivalent a la strategiePrudente, mais pour le joueur 2 : la matrice de gains doit etre construite differement, d'ou une fonction par joueur.
    if nbPierresCourant > 1 :
        matrice = []
        for i in range(nbPierresCourantAdversaire) :
            col = []
            for j in range(nbPierresCourant) :
                col.append(float("inf"))
            matrice.append(col)
        simplex.MatriceGainsJoueur2(nbPierresCourant,nbPierresCourantAdversaire,positionTroll,nbCases,matrice)
        s = simplex.SimplexGainsMatrice(nbPierresCourantAdversaire,nbPierresCourant,matrice)
        probabilitesStrategieMixte = s.x 
        print(probabilitesStrategieMixte)
        probasSansGain = np.delete(probabilitesStrategieMixte,len(probabilitesStrategieMixte)-1)
        i = np.random.choice(len(probasSansGain),p=probasSansGain)
        return nbPierresCourantAdversaire - i
    else :
        return 1