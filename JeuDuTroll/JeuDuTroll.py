# module qui met en place l'ensemble de l'environnement du jeu du troll, ainsi que le lancement des parties
import Strategies as strat

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
            CoupJ1 = strat.StrategieMixteOptimale2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
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
            #CoupJ2 = strat.StrategiePrudentePure(_pierresJ2Depart,plateau.nbCases,plateau.nbPierresJoueur2)
            CoupJ2 = strat.StrategieAleatoire(plateau.nbPierresJoueur2)
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
