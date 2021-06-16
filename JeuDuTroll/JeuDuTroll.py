# module qui met en place l'ensemble de l'environnement du jeu du troll, ainsi que le lancement des parties
import Strategies as strat
import threading
import multiprocessing
import time

s1 = 0 # nombre de fois ou la strategie du joueur 1 a gagne 
s2 = 0 # nombre de fois ou la strategie du joueur 2 a gagne
matchsNuls = 0 # nombre de matchs nuls
lock = threading.Lock() # semaphore pour les threads, pour pouvoir incrémenter les compteurs de victoire de façon concurrente.

class Plateau : #Objet qui va contenir une situation de jeu (nombre de pierres pour chaque joueur, nombre de cases, position du troll.
    nbCases = 7
    posTroll = 4
    nbPierresJoueur1 = 15
    nbPierresJoueur2 = 15


    def __init__(self, _nbCases, _posTrollDepart, _pierresJ1Depart, _pierresJ2Depart):
        self.nbCases = _nbCases
        self.posTroll = _posTrollDepart
        self.nbPierresJoueur1 = _pierresJ1Depart
        self.nbPierresJoueur2 = _pierresJ2Depart







def Partie(mode,_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart,CoupsJ1 = [],CoupsJ2 = []) : # Lancement d'une partie en fonction du mode de jeu (combien de joueurs), des differents parametres de jeu et de deux tableaux, en reference, pour l'historique des coups joues
    plateau = Plateau(_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart)
    print(plateau.nbCases," ",plateau.posTroll," ",plateau.nbPierresJoueur1," ",plateau.nbPierresJoueur2) # affichage de la situation initiale
    fin = False
    while not fin :
        print(plateau.nbCases, "cases, Troll a la position : ", plateau.posTroll, " J1 : ",plateau.nbPierresJoueur1," pierres, J2 : ",plateau.nbPierresJoueur2," pierres") #affichage de la situation courante

        if mode < 2 : # La variable "mode" de la Partie : 0 = 2 joueurs, 1 = 1 joueur face a une IA, 2 = 2 IAs.
            bon = False
            while not bon :
                print("Joueur 1, rentrez une valeur !")
                StrCoupJ1 = input()
                try : #saisie du coup par le joueur 1
                     CoupJ1 = int(StrCoupJ1)
                     if CoupJ1 <= plateau.nbPierresJoueur1 and CoupJ1 > 0 :
                         bon = True
                except ValueError:
                    print("entrez une valeur entiere svp")
            CoupsJ1.append(CoupJ1)
        else :  # si ce n'est pas un joueur, il faut appeler une fonction qui renvoie le nombre de pierres lancees, elle sont dans le module Strategies.
            #CoupJ1 = strat.StrategieAleatoire(plateau.nbPierresJoueur1)
            CoupJ1 = strat.StrategieMixteOptimale(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ1 = strat.Strategie1(15,7,plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.posTroll,1)
            CoupsJ1.append(CoupJ1)

        if mode == 0 :
            bon = False
            while not bon :
                print("Joueur 2, rentrez une valeur !")
                StrCoupJ2 = input()
                try : #saisie du coup par le joueur 2
                     CoupJ2 = int(StrCoupJ2)
                     if CoupJ2 <= plateau.nbPierresJoueur2 and CoupJ2 > 0 :
                         bon = True
                except ValueError:
                    print("entrez une valeur entiere svp")
            CoupsJ2.append(CoupJ2)
        else : # si ce n'est pas un joueur, il faut appeler une fonction qui renvoie le nombre de pierres lancees, elle sont dans le module Strategies.
            CoupJ2 = strat.StrategieAleatoire(plateau.nbPierresJoueur2)
            #CoupJ2 = strat.StrategiePrudentePure(15,7,plateau.nbPierresJoueur2)
            #CoupJ2 = strat.Strategie1(15,7,plateau.nbPierresJoueur2,plateau.nbPierresJoueur1,plateau.posTroll,2)
            CoupsJ2.append(CoupJ2)
        plateau.nbPierresJoueur1 -= CoupJ1
        plateau.nbPierresJoueur2 -= CoupJ2
        if CoupJ1 > CoupJ2:
            plateau.posTroll += 1 
        elif CoupJ1 < CoupJ2:
            plateau.posTroll -= 1 
        if (plateau.nbPierresJoueur1 <= 0 or plateau.nbPierresJoueur2 <= 0 or plateau.posTroll == plateau.nbCases or plateau.posTroll == 1) : # Si un joueur n'a plus de pierre, ou si le troll est arrive a destination, la partie s'arrete. 
            fin = True
    return ElectionJoueurGagnant(plateau) # 1 = joueur 1 a gagne, 2 = joueur 2 a gagne, 0 = match nul



def ElectionJoueurGagnant (plateau) : 
    if plateau.posTroll == 1 : # conditions de victoire en fonction de la position du troll
        print("Joueur 2 gagne ! ")
        return 2
    elif plateau.posTroll == plateau.nbCases :
        print("Joueur 1 gagne ! ")
        return 1
    else : # si le troll n'est pas arrive a destination, deplacement du trol en fonction du reste de pierres de chaque joueur, puis election du vainqueur en fonction de la position finale du troll.
        if plateau.nbPierresJoueur1 <= 0 :
            plateau.posTroll -= plateau.nbPierresJoueur2
        elif plateau.nbPierresJoueur2 <= 0 :
            plateau.posTroll += plateau.nbPierresJoueur1
        print("Troll position : ",plateau.posTroll)
        if plateau.posTroll <= plateau.nbCases//2 :
            print("Joueur 2 gagne !")
            return 2
        elif plateau.posTroll == (plateau.nbCases//2) + 1 :
            print("Match nul !")
            return 0
        else :
            print("Joueur 1 gagne !")
            return 1


def ConfigPartie(CoupsJ1 = [],CoupsJ2 = []) : # Configuration complete d'une partie par un terminal. Il est possible de passer cette etape et de directement appeler la fonction Partie.
    bon = False
    bonModeDeJeu = False
    bonJoueur1 = False
    bonCases = False
    bonTroll = False
    bonJoueur2 = False
    while not bon :
        while not bonModeDeJeu : 
            print("selection mode de jeu : 0 = 2 joueurs, 1 = joueur VS IA, 2 = IA VS IA ")
            SelectModeDeJeu = input()
            try :
                    SMDJ = int(SelectModeDeJeu)
                    if SMDJ >= 0 and SMDJ <= 2 :
                        bonModeDeJeu = True
            except ValueError:
                print("0 = 2 joueurs, 1 = joueur VS IA, 2 = IA VS IA")
        while not bonCases : 
            print("selection du nombre de cases de la partie")
            cases = input()
            try :
                nbCases = int(cases)
                if nbCases >= 3 :
                    bonCases = True
            except ValueError:
                print("Error")

        while not bonTroll : 
            print("selection de la position initiale du troll")
            troll = input()
            try :
                posTroll = int(troll)
                if posTroll > 1 and posTroll < nbCases :
                    bonTroll = True
            except ValueError:
                print("Error")

        while not bonJoueur1 : 
            print("selection du nombre de pierres pour le joueur 1")
            pierresJoueur1 = input()
            try :
                nbPierresJoueur1 = int(pierresJoueur1)
                if nbPierresJoueur1 >= 1 :
                    bonJoueur1 = True
            except ValueError:
                print("Error")
    
        while not bonJoueur2 : 
            print("selection du nombre de pierres pour le joueur 2")
            pierresJoueur2 = input()
            try :
                nbPierresJoueur2 = int(pierresJoueur2)
                if nbPierresJoueur2 >= 1 :
                    bonJoueur2 = True
            except ValueError:
                print("Error")
        bon = bonCases and bonModeDeJeu and bonTroll and bonJoueur1 and bonJoueur2
    
    return Partie(SMDJ,nbCases,posTroll,nbPierresJoueur1,nbPierresJoueur2, CoupsJ1, CoupsJ2)






def BoucleExecutionsThread() : # Fonction executee par un thread, equivalent a la boucle de la fonction main().
    CoupsJ1 = []
    CoupsJ2 = []
    global s1
    global s2
    global matchsNuls
    victoire = Partie(2,7,4,15,15,CoupsJ1,CoupsJ2)
    print("Liste des coups du joueur 1 : ",CoupsJ1)
    print("Liste des coups du joueur 2 : ",CoupsJ2)
    if victoire == 0 :
        lock.acquire() # verrouille le semaphore pour pouvoir changer une variable globale
        s1 += 0
        s2 += 0
        matchsNuls += 1
        lock.release() # deverrouille le semaphore pour pouvoir changer une variable globale 
    elif victoire == 1 :
        lock.acquire()
        s1 += 1
        lock.release()
    else :
        lock.acquire()
        s2 += 1
        lock.release()


def mainAsynchrone() : # Un exemple de main alternatif, qui peut être execute a la place de la fonction main, pour reduire les temps de calcul sur de grandes valeurs d'iteration.
    threads = [] # Tous les threads en cours d'execution
    #start = time.perf_counter() # timestamp de debut de programme pour mesurer le temps d'execution 
    for i in range(100): # 100 * nombre de coeurs executions.
        for k in range (multiprocessing.cpu_count()) : # on va lancer un thread par coeur logique du processeur car il n'est pas pertinent d'en lancer plus a la fois 
            t = threading.Thread(target=BoucleExecutionsThread) # creation du thread qui pointe vers la fonction qu'il devra executer
            t.start() # lancement du thread
            threads.append(t) # ajout dans le tableau des processus en cours d'execution.
        for k in range(multiprocessing.cpu_count()) : # On attend que tous les processus aient termines
            threads[k].join()
        threads.clear() # on rafraichit le tableau de threads
    print("Score : ","Strategie 1 : ", s1, " Strategie 2 : ", s2, " Matchs nuls : ", matchsNuls) # Statistiques finales
    #finish = time.perf_counter() # timestamp de fin de programme pour mesurer le temps d'execution 
    #print("Finished in : ", round(finish-start,2)," seconds " ) # temps d'execution





def main() : # programme principal, en synchrone, pertinent pour l'affichage de toutes les etapes. Suivant le nombre de parties jouees, la fonction peut avoir un temps d'execution tres long, d'où une version asynchrone.
    count = 0
    global s1
    global s2 # recuperation des variables globales s1, s2 et matchsNuls.
    global matchsNuls # passage en variables globales pour pouvoir etre accedes par les threads de la version asynchrone
    CoupsJ1 = []
    CoupsJ2 = []
    # start = time.perf_counter() # timestamp de debut de programme pour mesurer le temps d'execution
    for k in range (0,1000,1) : # iteration sur le nombre de parties
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = Partie(2,7,4,15,15,CoupsJ1,CoupsJ2) # 0 = nul, 1 = victoire J1, 2 = victoire J2
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
    #finish = time.perf_counter() # timestamp de fin de programme pour mesurer le temps d'execution 
    #print("Finished in : ", round(finish-start,2)," seconds " )








main()