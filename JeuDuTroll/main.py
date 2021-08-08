import JeuDuTroll as troll
import Exercice4 as exo4
import time
import numpy as np

s1 = 0 # nombre de fois ou la strategie du joueur 1 a gagne 
s2 = 0 # nombre de fois ou la strategie du joueur 2 a gagne
matchsNuls = 0 # nombre de matchs nuls

# Parametres du jeu 
ModeDeJeu = 2
NbCases = 7
PositionTroll = 4
NbPierresJ1 = 20
NbPierresJ2 = 20 # Pour changer la strategie de chaque joueur, il faut changer la fonction en commentaire dans JeuDuTroll pour chaque joueur.



def Exercice1() :
    print("_____________Exercice 1_________________")
    res = troll.strat.simplex.ProbasPourUneSituationDeJeu(25,21,3,7) # Dans notre implémentation, les cases vont de 1 à 7, donc le troll en position 4 correspond a la position 0 du TP et 3 a la position -1.
    probasSansGains = np.delete(res.x,len(res.x)-1) # on enleve la valeur du gain a la resolution du simplex.
    print("La distribution de probabilites est la suivante : ")
    print(probasSansGains)
    print("le gain est le suivant : ")
    print(res.x[len(res.x)-1])
    print("______________________________")
    nbPierresJ2 = 1
    gains = 1
    while True :
        res = troll.strat.simplex.ProbasPourUneSituationDeJeu(25,nbPierresJ2,3,7)
        gains = res.x[len(res.x)-1]
        if gains < 0 :
            break
        nbPierresJ2 += 1
    print(" dans la configuration (20,x,-1), le joueur 1 est désavantagé a partir de x = ",nbPierresJ2)

def Exercice3(nbPierresJ1 = 20,nbPierresJ2=20,posTroll=4,nbCases=7) :
    print("_____________Exercice 3_________________")
    matrice = []
    for i in range(nbPierresJ1) :
        col = []
        for j in range(nbPierresJ2) :
            col.append(float("inf"))
        matrice.append(col)
    troll.strat.simplex.MatriceGains(nbPierresJ1,nbPierresJ2,posTroll,nbCases,matrice) # calcul matrice de gains
    probas = troll.strat.simplex.solve(matrice) # calcul des differentes probabilites de jouer une situation donnee
    probasSansGain = np.delete(probas.x,len(probas.x)-1) # retrait du gain (il s'agit du gain dans le pire des cas, nous, nous cherchons le gain lorsque le joueur adverse joue aleatoirement
    gains = 0
    nbMaxPierresLanceesJ2 = nbPierresJ2//3
    nbPierresRestantesJ2 = nbPierresJ2 - nbMaxPierresLanceesJ2
    probasLancerPierres = 1/nbMaxPierresLanceesJ2
    for i in range(len(matrice)):
        proba = probasSansGain[len(probasSansGain)-1]
        sum = 0
        for j in range(len(matrice[0])) : 
# avec Pi la probabilite de lancer n1-i pierres pour le joueur1,Pj la probabilite de lancer n2-j pierres pour le joueur2, et Gij le gain quand il reste i pierres au J1 et j pierres au J2, G = somme des i (Xi*(somme des j (Xj*Gij)))
            if j >= nbPierresRestantesJ2: # Sinon, la probabilite de lancer est de 0 pour le joueur 2.
                sum += matrice[i][j] * probasLancerPierres
        gains += sum * probasSansGain[i]
    print("gains contre la strategie aleatoire n/3 : ",gains)


def Exercice4(x = 20, y = 20, positionTroll = 4, cases = 7) :
    print("_____________Exercice 4 _______________")
    print("_____________Cas coup J2 impair _______________")
    matrice = []
    for i in range(x) :
        col = []
        for j in range(y) :
            col.append(float("inf"))
        matrice.append(col)

    exo4.MatriceGainsImpair(x,y,positionTroll,cases,matrice)
    matTmp = []
    for i in range(len(matrice)) :
        col = []
        for j in range (len(matrice[0])) :
            if (y - j) % 2 == 1 :
                col.append(matrice[i][j])
        matTmp.append(col)
    res = troll.strat.simplex.solve(matTmp)
    probasSansGains = np.delete(res.x,len(res.x)-1) # on enleve la valeur du gain a la resolution du simplex.
    print("La distribution de probabilites est la suivante : ")
    print(probasSansGains)
    print("le gain est le suivant : ")
    print(res.x[len(res.x)-1])
    print("______________________________")
    nbPierresJ2 = 20
    gains = 1
    while True :
        matrice = []
        for i in range(x) :
            col = []
            for j in range(nbPierresJ2) :
                col.append(float("inf"))
            matrice.append(col)
        exo4.MatriceGainsImpair(x,nbPierresJ2,positionTroll,cases,matrice)
        matTmp = []
        for i in range(len(matrice)) :
            col = []
            for j in range (len(matrice[0])) :
                if (nbPierresJ2 - j) % 2 == 1 :
                    col.append(matrice[i][j])
            matTmp.append(col)
        res = troll.strat.simplex.solve(matTmp)
        gains = res.x[len(res.x)-1]
        print(gains)
        if gains < 0 :
            break
        nbPierresJ2 += 1
    print(" dans la configuration (20,x,-1), le joueur 1 est désavantagé a partir de x = ",nbPierresJ2," en appliquant la regle des 2 cases ")

    print("_____________Cas troll avance de 2 cases _______________")
    matrice = []
    for i in range(x) :
        col = []
        for j in range(y) :
            col.append(float("inf"))
        matrice.append(col)

    exo4.MatriceGains2Cases(x,y,positionTroll,cases,matrice)
    res = troll.strat.simplex.solve(matrice)
    probasSansGains = np.delete(res.x,len(res.x)-1) # on enleve la valeur du gain a la resolution du simplex.
    print("La distribution de probabilites est la suivante : ")
    print(probasSansGains)
    print("le gain est le suivant : ")
    print(res.x[len(res.x)-1])
    print("______________________________")
    nbPierresJ2 = 30
    gains = 1
    while True :
        matrice = []
        for i in range(x) :
            col = []
            for j in range(nbPierresJ2) :
                col.append(float("inf"))
            matrice.append(col)
        exo4.MatriceGains2Cases(x,nbPierresJ2,positionTroll,cases,matrice)
        res = troll.strat.simplex.solve(matrice)
        gains = res.x[len(res.x)-1]
        print(gains)
        if gains < 0 :
            break
        nbPierresJ2 += 1
    print(" dans la configuration (20,x,-1), le joueur 1 est désavantagé a partir de x = ",nbPierresJ2, " en appliquant la regle des 2 cases ")



def main() : # programme principal, en synchrone, pertinent pour l'affichage de toutes les etapes. Suivant le nombre de parties jouees, la fonction peut avoir un temps d'execution tres long, d'où une version asynchrone.
    global s1
    global s2 # recuperation des variables globales s1, s2 et matchsNuls.
    global matchsNuls # passage en variables globales pour pouvoir etre accedes par les threads de la version asynchrone
    CoupsJ1 = []
    CoupsJ2 = []
    start = time.perf_counter() # timestamp de debut de programme pour mesurer le temps d'execution
    for k in range (10) : # iteration sur le nombre de parties, augmenter ce chiffre augmentera fortement le temps d'execution
        print ("iteration n° ", k+1)
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = troll.Partie(ModeDeJeu,NbCases,PositionTroll,NbPierresJ1,NbPierresJ2,CoupsJ1,CoupsJ2) # 0 = nul, 1 = victoire J1, 2 = victoire J2 | mode,nombre de cases,position du troll, nombre de pierres par joueur, historique 
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
    print(20//3)



#main()
#Exercice1()
#Exercice3()
Exercice4()
