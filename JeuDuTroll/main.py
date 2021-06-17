import JeuDuTroll as troll
import threading
import multiprocessing
import time

s1 = 0 # nombre de fois ou la strategie du joueur 1 a gagne 
s2 = 0 # nombre de fois ou la strategie du joueur 2 a gagne
matchsNuls = 0 # nombre de matchs nuls
lock = threading.Lock() # semaphore pour les threads, pour pouvoir incrémenter les compteurs de victoire de façon concurrente.

def BoucleExecutionsThread() : # Fonction executee par un thread, equivalent a la boucle de la fonction main().
    CoupsJ1 = []
    CoupsJ2 = []
    global s1
    global s2
    global matchsNuls
    victoire = troll.Partie(2,7,4,15,15,CoupsJ1,CoupsJ2)
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
    for k in range (1000) : # iteration sur le nombre de parties
        CoupsJ1 = []
        CoupsJ2 = []
        victoire = troll.Partie(2,7,4,15,15,CoupsJ1,CoupsJ2) # 0 = nul, 1 = victoire J1, 2 = victoire J2
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
