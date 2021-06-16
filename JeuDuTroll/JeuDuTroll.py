import Strategies as strat
import threading
import multiprocessing
import time

s1 = 0
s2 = 0
matchsNuls = 0
lock = threading.Lock()

class Plateau :
    nbCases = 7
    posTroll = 4
    nbPierresJoueur1 = 15
    nbPierresJoueur2 = 15


    def __init__(self, _nbCases, _posTrollDepart, _pierresJ1Depart, _pierresJ2Depart):
        self.nbCases = _nbCases
        self.posTroll = _posTrollDepart
        self.nbPierresJoueur1 = _pierresJ1Depart
        self.nbPierresJoueur2 = _pierresJ2Depart







def Partie(mode,_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart,CoupsJ1,CoupsJ2) :
    plateau = Plateau(_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart)
    print(plateau.nbCases," ",plateau.posTroll," ",plateau.nbPierresJoueur1," ",plateau.nbPierresJoueur2)
    fin = False
    while not fin :
        print(plateau.nbCases, "cases, Troll a la position : ", plateau.posTroll, " J1 : ",plateau.nbPierresJoueur1," pierres, J2 : ",plateau.nbPierresJoueur2," pierres")

        if mode < 2 :
            bon = False
            while not bon :
                print("Joueur 1, rentrez une valeur !")
                StrCoupJ1 = input()
                try :
                     CoupJ1 = int(StrCoupJ1)
                     if CoupJ1 <= plateau.nbPierresJoueur1 and CoupJ1 > 0 :
                         bon = True
                except ValueError:
                    print("entrez une valeur entiere svp")
            CoupsJ1.append(CoupJ1)
        else :
            #CoupJ1 = strat.StrategieAleatoire(plateau.nbPierresJoueur1)
            CoupJ1 = strat.StrategieMixteOptimale(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ1 = strat.Strategie1(15,7,plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.posTroll,1)
            CoupsJ1.append(CoupJ1)

        if mode == 0 :
            bon = False
            while not bon :
                print("Joueur 2, rentrez une valeur !")
                StrCoupJ2 = input()
                try :
                     CoupJ2 = int(StrCoupJ2)
                     if CoupJ2 <= plateau.nbPierresJoueur2 and CoupJ2 > 0 :
                         bon = True
                except ValueError:
                    print("entrez une valeur entiere svp")
            CoupsJ2.append(CoupJ2)
        else :
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
        if (plateau.nbPierresJoueur1 <= 0 or plateau.nbPierresJoueur2 <= 0 or plateau.posTroll == plateau.nbCases or plateau.posTroll == 1) :
            fin = True
    return ElectionJoueurGagnant(plateau)



def ElectionJoueurGagnant (plateau) : 
    if plateau.posTroll == 1 :
        print("Joueur 2 gagne ! ")
        return 2
    elif plateau.posTroll == plateau.nbCases :
        print("Joueur 1 gagne ! ")
        return 1
    else :
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


def ConfigPartie(CoupsJ1,CoupsJ2) :
    bon = False
    while not bon :
            print("selection mode de jeu : 0 = 2 joueurs, 1 = joueur VS IA, 2 = IA VS IA ")
            SelectModeDeJeu = input()
            try :
                 SMDJ = int(SelectModeDeJeu)
                 if SMDJ >= 0 and SMDJ <= 2 :
                     bon = True
            except ValueError:
                print("0 = 2 joueurs, 1 = joueur VS IA, 2 = IA VS IA")
    
    return Partie(SMDJ, CoupsJ1, CoupsJ2)






def BoucleExecutionsThread() :
    CoupsJ1 = []
    CoupsJ2 = []
    global s1
    global s2
    global matchsNuls
    victoire = Partie(2,CoupsJ1,CoupsJ2)
    print("Liste des coups du joueur 1 : ",CoupsJ1)
    print("Liste des coups du joueur 2 : ",CoupsJ2)
    if victoire == 0 :
        lock.acquire()
        s1 += 0
        s2 += 0
        matchsNuls += 1
        lock.release()
    elif victoire == 1 :
        lock.acquire()
        s1 += 1
        lock.release()
    else :
        lock.acquire()
        s2 += 1
        lock.release()


def mainAsynchrone() :
    count = 0
    threads = []
    start = time.perf_counter()
    for i in range(100):
        for k in range (multiprocessing.cpu_count()) :
            t = threading.Thread(target=BoucleExecutionsThread)
            t.start()
            threads.append(t)
        for k in range(multiprocessing.cpu_count()) :
            threads[k].join()
        threads.clear()
    print("Score : ","Strategie 1 : ", s1, " Strategie 2 : ", s2, " Matchs nuls : ", matchsNuls)
    finish = time.perf_counter()
    print("Finished in : ", round(finish-start,2)," seconds " )





def main() :
    count = 0
    global s1
    global s2
    global matchsNuls
    CoupsJ1 = []
    CoupsJ2 = []
    start = time.perf_counter()
    for k in range (0,1000,1) :
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = Partie(2,7,4,15,15,CoupsJ1,CoupsJ2)
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
    finish = time.perf_counter()
    print("Finished in : ", round(finish-start,2)," seconds " )






main()