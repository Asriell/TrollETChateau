import JeuDuTroll as troll
import numpy as np
import time

s1 = 0 # nombre de fois ou la strategie du joueur 1 a gagne 
s2 = 0 # nombre de fois ou la strategie du joueur 2 a gagne
matchsNuls = 0 # nombre de matchs nuls

# Parametres du jeu 
ModeDeJeu = 2
NbCases = 5
PositionTroll = 3
NbPierresJ1 = 20
NbPierresJ2 = 20 # Pour changer la strategie de chaque joueur, il faut changer la fonction en commentaire dans JeuDuTroll pour chaque joueur.
ProbaSuccesJ2 = 0.5


def Exercice3(nbPierresJ1 = 20,nbPierresJ2=20,posTroll=3,nbCases=5) :
    print("_____________Exercice 3_________________")
    matrice = []
    for i in range(nbPierresJ1) :
        col = []
        for j in range(nbPierresJ2) :
            col.append(float("inf"))
        matrice.append(col)

    troll.strat.simplex.MatriceGains(nbPierresJ1,nbPierresJ2,posTroll,nbCases,matrice) # calcul matrice de gains
    probas = troll.strat.simplex.solve(matrice) # calcul des differentes probabilites de jouer une situation donnee
    #print(probas)
    probasSansGain = np.delete(probas.x,len(probas.x)-1) # retrait du gain (il s'agit du gain dans le pire des cas, nous, nous cherchons le gain lorsque le joueur adverse joue aleatoirement
    gains = 0
    nbMaxPierresLanceesJ2 = nbPierresJ2//3
    nbPierresRestantesJ2 = nbPierresJ2 - nbMaxPierresLanceesJ2
    probasLancerPierres = 1/nbMaxPierresLanceesJ2
    print("pierres restantes : ",nbPierresRestantesJ2)
    print("pierres lancees : ",nbMaxPierresLanceesJ2)
    print("pierres lancees : ",probasLancerPierres)
    for i in range(len(matrice)):
        proba = probasSansGain[len(probasSansGain)-1]
        sum = 0
        for j in range(len(matrice[0])) : 
# avec Pi la probabilite de lancer n1-i pierres pour le joueur1,Pj la probabilite de lancer n2-j pierres pour le joueur2, et Gij le gain quand il reste i pierres au J1 et j pierres au J2, G = somme des i (Xi*(somme des j (Xj*Gij)))
            if j >= nbPierresRestantesJ2: # Sinon, la probabilite de lancer est de 0 pour le joueur 2.
                sum += matrice[i][j] * probasLancerPierres
        gains += sum * probasSansGain[i]
    print("gains contre la strategie aleatoire n/3 : ",gains)


    


def Exercice1() :
    print("_____________Exercice 1_________________")
    res = troll.strat.simplex.ProbasPourUneSituationDeJeu(23,20,2,5)
    probasSansGain = np.delete(res.x,len(res.x)-1)
    print("La distribution de probabilites est la suivante : ")
    print(probasSansGain)
    print("le gain est le suivant : ")
    print(res.x[len(res.x)-1])
    print("______________________________")
    nbPierresJ2 = 1
    gains = 1
    while True :
        res = troll.strat.simplex.ProbasPourUneSituationDeJeu(20,nbPierresJ2,2,5)
        gains = res.x[len(res.x)-1]
        if gains < 0 :
            break
        nbPierresJ2 += 1
    print(" dans la configuration (20,x,-1), le joueur 1 est désavantagé a partir de x = ",nbPierresJ2)
    




def Exercice4() :
    nbPierresJ2 = 1
    gains = 1
    while True :
        res = troll.strat.simplex.ProbasPourUneSituationDeJeuModifiee(20,nbPierresJ2,3,5)
        gains = res.x[len(res.x)-1]
        print("x : ",nbPierresJ2," gains : ",gains)
        if gains < 0 :
            break
        nbPierresJ2 += 1
    print(" dans la configuration (20,x,-1), le joueur 1 est désavantagé a partir de x = ",nbPierresJ2) # gains négatifs pour x = 56

def main() : # programme principal, en synchrone, pertinent pour l'affichage de toutes les etapes. Suivant le nombre de parties jouees, la fonction peut avoir un temps d'execution tres long, d'où une version asynchrone.
    global s1
    global s2 # recuperation des variables globales s1, s2 et matchsNuls.
    global matchsNuls # passage en variables globales pour pouvoir etre accedes par les threads de la version asynchrone
    CoupsJ1 = []
    CoupsJ2 = []
    start = time.perf_counter() # timestamp de debut de programme pour mesurer le temps d'execution
    for k in range (1000) : # iteration sur le nombre de parties, augmenter ce chiffre augmentera fortement le temps d'execution
        print ("iteration n° ", k+1)
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = troll.PartieModifiee(ModeDeJeu,NbCases,PositionTroll,NbPierresJ1,NbPierresJ2,ProbaSuccesJ2,CoupsJ1,CoupsJ2) # 0 = nul, 1 = victoire J1, 2 = victoire J2 | mode,nombre de cases,position du troll, nombre de pierres par joueur, historique 
        print("Liste des coups du joueur 1 : ",CoupsJ1)
        print("Liste des coups du joueur 2 : ",CoupsJ2)
        if victoire == 0 :
            s1 += 0
            s2 += 0
            matchsNuls += 1
        elif victoire == 1 :
            s1 += 1
        else :
            s2 += 1
        print("Score : ","Strategie 1 : ", s1, " Strategie 2 : ", s2, " Matchs nuls : ", matchsNuls)
    print("Score final : ","Strategie 1 : ", s1, " Strategie 2 : ", s2, " Matchs nuls : ", matchsNuls)
    finish = time.perf_counter() # timestamp de fin de programme pour mesurer le temps d'execution 
    print("Finished in : ", round(finish-start,2)," seconds " )








#main()
Exercice4()
