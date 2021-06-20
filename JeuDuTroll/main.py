import JeuDuTroll as troll
import time

s1 = 0 # nombre de fois ou la strategie du joueur 1 a gagne 
s2 = 0 # nombre de fois ou la strategie du joueur 2 a gagne
matchsNuls = 0 # nombre de matchs nuls





def main() : # programme principal, en synchrone, pertinent pour l'affichage de toutes les etapes. Suivant le nombre de parties jouees, la fonction peut avoir un temps d'execution tres long, d'où une version asynchrone.
    global s1
    global s2 # recuperation des variables globales s1, s2 et matchsNuls.
    global matchsNuls # passage en variables globales pour pouvoir etre accedes par les threads de la version asynchrone
    CoupsJ1 = []
    CoupsJ2 = []
    start = time.perf_counter() # timestamp de debut de programme pour mesurer le temps d'execution
    for k in range (100) : # iteration sur le nombre de parties, augmenter ce chiffre augmentera fortement le temps d'execution
        print ("iteration n° ", k+1)
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = troll.Partie(2,7,4,10,10,CoupsJ1,CoupsJ2) # 0 = nul, 1 = victoire J1, 2 = victoire J2 | mode,nombre de cases,position du troll, nombre de pierres par joueur, historique 
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








main()
