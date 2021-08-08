import JeuDuTroll as troll
import Strategies as strat
import Solveur as simplex

#Tout d'abord, le cas où le joueur ne peut lancer qu'un nombre impair de pierres : 

def PartieImpair(mode,_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart,CoupsJ1 = [],CoupsJ2 = []) : # Lancement d'une partie en fonction du mode de jeu (combien de joueurs), des differents parametres de jeu et de deux tableaux, en reference, pour l'historique des coups joues
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
            CoupJ1 = StrategiePrudenteImpair(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ1 = strat.StrategieContreExercice3(_pierresJ1Depart,plateau.nbPierresJoueur1)
            #CoupJ1 = strat.StrategieAgressive(_pierresJ1Depart,plateau.nbCases,plateau.nbPierresJoueur1)
            #CoupJ1 = strat.Strategie1(15,7,plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.posTroll,1)
            CoupsJ1.append(CoupJ1)

        if mode == 0 :
            bon = False
            while not bon :
                print("Joueur 2, rentrez une valeur !")
                StrCoupJ2 = input()
                try : #saisie du coup par le joueur 2
                     CoupJ2 = int(StrCoupJ2)
                     if CoupJ2 <= plateau.nbPierresJoueur2 and CoupJ2 > 0 and CoupJ2 % 2 == 1 :
                         bon = True
                except ValueError:
                    print("entrez une valeur entiere svp")
            CoupsJ2.append(CoupJ2)
        else : # si ce n'est pas un joueur, il faut appeler une fonction qui renvoie le nombre de pierres lancees, elle sont dans le module Strategies.
            bon = False
            stop = 0
            while not bon :
                #CoupJ2 = strat.StrategieAgressive(_pierresJ2Depart,plateau.nbCases,plateau.nbPierresJoueur2)
                CoupJ2 = strat.StrategieAleatoireExercice3(plateau.nbPierresJoueur2)
                #CoupJ2 = strat.StrategieContreExercice3(_pierresJ2Depart,plateau.nbPierresJoueur2)
                #CoupJ2 = strat.StrategiePrudenteJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
                #CoupJ2 = strat.Strategie1(15,7,plateau.nbPierresJoueur2,plateau.nbPierresJoueur1,plateau.posTroll,2)
                #CoupJ2 = strat.StrategiePrudenteNonLineaireJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
                stop += 1
                assert stop <= 500,"valeur impaire non trouvee"
                if CoupJ2 % 2 == 1 :
                    bon = True
            CoupsJ2.append(CoupJ2)
        plateau.nbPierresJoueur1 -= CoupJ1
        plateau.nbPierresJoueur2 -= CoupJ2
        if CoupJ1 > CoupJ2:
            plateau.posTroll += 1 
        elif CoupJ1 < CoupJ2:
            plateau.posTroll -= 1 
        if (plateau.nbPierresJoueur1 <= 0 or plateau.nbPierresJoueur2 <= 0 or plateau.posTroll == plateau.nbCases or plateau.posTroll == 1) : # Si un joueur n'a plus de pierre, ou si le troll est arrive a destination, la partie s'arrete. 
            fin = True
    return troll.ElectionJoueurGagnant(plateau) # 1 = joueur 1 a gagne, 2 = joueur 2 a gagne, 0 = match nul



def MatriceGainsImpair(nbPierresJ1, nbPierresJ2,positionTroll,nbCases,matrice) : # remplissage de la matrice de gains
    positionTrollInitiale = positionTroll - (nbCases//2 + 1 ) # 1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range (nbPierresJ1) :
        for j in range (nbPierresJ2) : # i = nb pierres restantes au J1, j = nb pierres restantes au J2
            t = positionTrollInitiale
            nbPierresLanceesJ1 = nbPierresJ1 - i
            nbPierresLanceesJ2 = nbPierresJ2 - j # pierres lancees = pierres initiales - pierres restantes, mouvement du troll en fonction.
            if nbPierresLanceesJ2 % 2 == 0 : # Cas impossible, on passe à la configuration d'apres.
                continue
            if nbPierresLanceesJ1 < nbPierresLanceesJ2 :
                t -= 1
            if nbPierresLanceesJ1 > nbPierresLanceesJ2 :
                t += 1
            if t <= -(nbCases//2) : # remplissage de la matrice pour tous les cas triviaux : D'abord les cas ou le deplacement de t menerait a la victoire
                matrice[i][j] = -1
            elif t >= (nbCases//2)-1 :
                matrice[i][j] = 1
            elif i == 0 : # Ensuite, le cas (0,j,t)
                if t > 0 :
                    if j == t :
                        matrice[i][j] = 0
                    elif j > t :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t < 0 :
                    matrice[i][j] = -1
                else :
                    if j == 0 :
                        matrice[i][j] = 0
                    else :
                        matrice[i][j] = -1
            elif j == 0 : # Ensuite, le cas (i,0,t)
                if t < 0 :
                    if i == abs(t) :
                        matrice[i][j] = 0
                    elif i < abs(t) :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t > 0 :
                    matrice[i][j] = 1
                else :
                    if i == 0 :
                        matrice[i][j] = 0
                    else :
                        matrice[i][j] = 1

            elif i == j :
                if t == 0:
                    matrice[i][j] = 0
                else :
                    matTmp = []
                    for iTmp in range(i):
                        col = []
                        for jTmp in range(j):
                            if (nbPierresJ2 - jTmp) % 2 == 1 :
                                col.append(matrice[iTmp][jTmp])
                        if col :
                            matTmp.append(col)
                    #print("Pour : ",nbPierresJ1, "  ", nbPierresJ2,"   ", positionTroll)
                    #print("Valeurs : ",i, "  ", j)
                    #for k in range (len(matrice)):
                    #    print("matrice : ",matrice[k])
                    #for k in range(len(matTmp)) :
                    #    print("mat tmp : " ,matTmp[k])
                    #print(len(matTmp))
                    if not matTmp : # signifie que le joueur ne peut lancer ses pierres qu'une par une
                        if t == 0 :
                            if i>j :
                             matrice[i][j] = 1
                            elif i == j : 
                                matrice[i][j] = 0
                            else :
                                matrice[i][j] = 0
                        elif t < 0 :
                            if (i-j) > abs(t) :
                                matrice[i][j] = 1
                            elif (i-j) == abs(t) :
                                matrice[i][j] = 0
                            else:
                                matrice[i][j] = -1
                        else:
                            if (j - i) > t :
                                matrice[i][j] = -1
                            elif (j-i) == t :
                                matrice[i][j] = 0
                            else:
                                return 1
                    else :
                        matrice[i][j] =  simplex.ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si les joueurs ont le même nombre de pierres, le cas est trivial si le troll est au milieu (pas d'avantage pour un joueur). Sinon, ce n'est plus un cas trivial.
            else : # Sinon
                matTmp = []
                for iTmp in range(i):
                    col = []
                    for jTmp in range(j):
                        if (nbPierresJ2 - jTmp) % 2 == 1 :
                            col.append(matrice[iTmp][jTmp])
                    if col : 
                        matTmp.append(col)
                #print("Pour : ",nbPierresJ1, "  ", nbPierresJ2,"   ", positionTroll)
                #print("Valeurs : ",i, "  ", j)
                #for k in range (len(matrice)):
                #    print("matrice : ",matrice[k])
                #for k in range(len(matTmp)) :
                #    print("mat tmp : " ,matTmp[k])
                if not matTmp  : # signifie que le joueur ne peut lancer ses pierres qu'une par une
                    if t == 0 :
                        if i>j :
                            matrice[i][j] = 1
                        elif i == j : 
                            matrice[i][j] = 0
                        else :
                            matrice[i][j] = 0
                    elif t < 0 :
                        if (i-j) > abs(t) :
                            matrice[i][j] = 1
                        elif (i-j) == abs(t) :
                            matrice[i][j] = 0
                        else:
                            matrice[i][j] = -1
                    else:
                        if (j - i) > t :
                            matrice[i][j] = -1
                        elif (j-i) == t :
                            matrice[i][j] = 0
                        else:
                            matrice[i][j] = 1
                else :
                    #print(matTmp)
                    matrice[i][j] = simplex.ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si on n'est pas dans un cas trivial, remplissage de la matrice par un simplex de sous-matrices deja calculees.
                #print(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp))
                #print(round(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp).x[len(matTmp)],10))
            #print("i = ",i," j = ",j, "t = ",t, " gain associe : ",matrice[i][j])


def StrategiePrudenteImpair(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) :
    #Calcul de la matrice de gains
    if nbPierresCourant > 1 : # Si il ne reste qu'une seule pierre, on peut retourner 1 directement.
        matrice = []
        for i in range(nbPierresCourant) :
            col = []
            for j in range(nbPierresCourantAdversaire) :
                col.append(float("inf"))
            matrice.append(col) # creation d'une matrice qui va stocker les gains.
        MatriceGainsImpair(nbPierresCourant,nbPierresCourantAdversaire,positionTroll,nbCases,matrice) # calcul de la matrice de gains en fonction du nombre de pierres lancees
        matTmp = [] # reduction de la matrice de gains en fonction de j.
        for i in range(len(matrice)) :
            col = []
            for j in range (len(matrice[0])) :
                if (nbPierresCourantAdversaire - j) % 2 == 1 :
                    col.append(matrice[i][j])
            matTmp.append(col)
        s = simplex.solve(matTmp) # simplex de la matrice du sous-jeu afin d'obtenir le gain et la distribution de probabilites des coups a jouer
        probabilitesStrategieMixte = s.x # distribution de probabilites des coups possibles, avec x[0] le cas ou le joueur lance toutes ses pierres et x[nbPierresCourant-1] le cas ou le joueur ne lance qu'une seule pierre.
        print(probabilitesStrategieMixte) # affichage de la distribution de probabilites, a commenter / decommenter au besoin.
        probasSansGain = np.delete(probabilitesStrategieMixte,len(probabilitesStrategieMixte)-1) #retrait de la valeur de gain, pour seulement avoir les différentes probabilites
        probasSansGain = list(map(lambda x: abs(x),probasSansGain))
        i = np.random.choice(len(probasSansGain),p=probasSansGain) #selection d'un indice selon les probabilites
        return nbPierresCourant - i #pierres du joueur - pierresRestantes apres lancer = nombre de pierres lancees
    else :
        return 1



# Cas où le troll avance de 2 cases si le joueur 1 lance 2 pierres de + minimum :

def Partie2Cases(mode,_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart,CoupsJ1 = [],CoupsJ2 = []) : # Lancement d'une partie en fonction du mode de jeu (combien de joueurs), des differents parametres de jeu et de deux tableaux, en reference, pour l'historique des coups joues
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
            CoupJ1 = strat.StrategiePrudente(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ1 = strat.StrategieContreExercice3(_pierresJ1Depart,plateau.nbPierresJoueur1)
            #CoupJ1 = strat.StrategieAgressive(_pierresJ1Depart,plateau.nbCases,plateau.nbPierresJoueur1)
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
            #CoupJ2 = strat.StrategieAgressive(_pierresJ2Depart,plateau.nbCases,plateau.nbPierresJoueur2)
            #CoupJ2 = strat.StrategieAleatoireExercice3(plateau.nbPierresJoueur2)
            CoupJ2 = strat.StrategieContreExercice3(_pierresJ2Depart,plateau.nbPierresJoueur2)
            #CoupJ2 = strat.StrategiePrudenteJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ2 = strat.Strategie1(15,7,plateau.nbPierresJoueur2,plateau.nbPierresJoueur1,plateau.posTroll,2)
            #CoupJ2 = strat.StrategiePrudenteNonLineaireJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            CoupsJ2.append(CoupJ2)
        plateau.nbPierresJoueur1 -= CoupJ1
        plateau.nbPierresJoueur2 -= CoupJ2
        if CoupJ1 > CoupJ2:
            if CoupJ1 >= (CoupJ2 + 2) :
                plateau.posTroll += 2
            else :
                plateau.posTroll += 1 
        elif CoupJ1 < CoupJ2:
            plateau.posTroll -= 1 
        if (plateau.nbPierresJoueur1 <= 0 or plateau.nbPierresJoueur2 <= 0 or plateau.posTroll == plateau.nbCases or plateau.posTroll == 1) : # Si un joueur n'a plus de pierre, ou si le troll est arrive a destination, la partie s'arrete. 
            fin = True
    return ElectionJoueurGagnant(plateau) # 1 = joueur 1 a gagne, 2 = joueur 2 a gagne, 0 = match nul


def MatriceGains2Cases(nbPierresJ1, nbPierresJ2,positionTroll,nbCases,matrice) : # remplissage de la matrice de gains
    positionTrollInitiale = positionTroll - (nbCases//2 + 1 ) # 1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range (nbPierresJ1) :
        for j in range (nbPierresJ2) : # i = nb pierres restantes au J1, j = nb pierres restantes au J2
            t = positionTrollInitiale
            nbPierresLanceesJ1 = nbPierresJ1 - i
            nbPierresLanceesJ2 = nbPierresJ2 - j # pierres lancees = pierres initiales - pierres restantes, mouvement du troll en fonction.
            if nbPierresLanceesJ1 < nbPierresLanceesJ2 :
                t -= 1
            if nbPierresLanceesJ1 > nbPierresLanceesJ2 :
                if nbPierresLanceesJ1 > (nbPierresLanceesJ2 + 2) :
                    t+=2
                else :
                    t += 1
            if t == -(nbCases//2) : # remplissage de la matrice pour tous les cas triviaux : D'abord les cas ou le deplacement de t menerait a la victoire
                matrice[i][j] = -1
            elif t == (nbCases//2)-1 :
                matrice[i][j] = 1
            elif i == 0 : # Ensuite, le cas (0,j,t)
                if t > 0 :
                    if j == t :
                        matrice[i][j] = 0
                    elif j > t :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t < 0 :
                    matrice[i][j] = -1
                else :
                    if j == 0 :
                        matrice[i][j] = 0
                    else :
                        matrice[i][j] = -1
            elif j == 0 : # Ensuite, le cas (i,0,t)
                if t < 0 :
                    if i == abs(t) :
                        matrice[i][j] = 0
                    elif i < abs(t) :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t > 0 :
                    matrice[i][j] = 1
                else :
                    if i == 0 :
                        matrice[i][j] = 0
                    else :
                        matrice[i][j] = 1

            elif i == j :
                if t == 0:
                    matrice[i][j] = 0
                else :
                    matTmp = []
                    for iTmp in range(i):
                        col = []
                        for jTmp in range(j):
                            col.append(matrice[iTmp][jTmp])
                        matTmp.append(col)
                    matrice[i][j] =  simplex.ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si les joueurs ont le même nombre de pierres, le cas est trivial si le troll est au milieu (pas d'avantage pour un joueur). Sinon, ce n'est plus un cas trivial.
            else : # Sinon
                matTmp = []
                for iTmp in range(i):
                    col = []
                    for jTmp in range(j):
                        col.append(matrice[iTmp][jTmp])
                    matTmp.append(col)
                #print("Pour : ",nbPierresJ1, "  ", nbPierresJ2,"   ", positionTroll)
                #print("Valeurs : ",i, "  ", j)
                #for k in range (len(matrice)):
                #    print("matrice : ",matrice[k])
                #for k in range(len(matTmp)) :
                #    print("mat tmp : " ,matTmp[k])
                matrice[i][j] = simplex.ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si on n'est pas dans un cas trivial, remplissage de la matrice par un simplex de sous-matrices deja calculees.
                #print(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp))
                #print(round(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp).x[len(matTmp)],10))
            #print("i = ",i," j = ",j, "t = ",t, " gain associe : ",matrice[i][j])



def StrategiePrudente2Cases(nbPierresCourant,nbPierresCourantAdversaire,nbCases,positionTroll) :
    #Calcul de la matrice de gains
    if nbPierresCourant > 1 : # Si il ne reste qu'une seule pierre, on peut retourner 1 directement.
        matrice = []
        for i in range(nbPierresCourant) :
            col = []
            for j in range(nbPierresCourantAdversaire) :
                col.append(float("inf"))
            matrice.append(col) # creation d'une matrice qui va stocker les gains.
        MatriceGains2Cases(nbPierresCourant,nbPierresCourantAdversaire,positionTroll,nbCases,matrice) # calcul de la matrice de gains en fonction du nombre de pierres lancees
        s = simplex.solve(matrice) # simplex de la matrice du sous-jeu afin d'obtenir le gain et la distribution de probabilites des coups a jouer
        probabilitesStrategieMixte = s.x # distribution de probabilites des coups possibles, avec x[0] le cas ou le joueur lance toutes ses pierres et x[nbPierresCourant-1] le cas ou le joueur ne lance qu'une seule pierre.
        print(probabilitesStrategieMixte) # affichage de la distribution de probabilites, a commenter / decommenter au besoin.
        probasSansGain = np.delete(probabilitesStrategieMixte,len(probabilitesStrategieMixte)-1) #retrait de la valeur de gain, pour seulement avoir les différentes probabilites
        probasSansGain = list(map(lambda x: abs(x),probasSansGain))
        i = np.random.choice(len(probasSansGain),p=probasSansGain) #selection d'un indice selon les probabilites
        return nbPierresCourant - i #pierres du joueur - pierresRestantes apres lancer = nombre de pierres lancees
    else :
        return 1



# Cas où le joueur 2 vise mal :

def PartieViseMal(mode,_nbCases,_posTrollDepart,_pierresJ1Depart,_pierresJ2Depart,probaToucherJ2,CoupsJ1 = [],CoupsJ2 = []) : # Lancement d'une partie en fonction du mode de jeu (combien de joueurs), des differents parametres de jeu et de deux tableaux, en reference, pour l'historique des coups joues
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
            CoupJ1 = strat.StrategiePrudente(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ1 = strat.StrategieContreExercice3(_pierresJ1Depart,plateau.nbPierresJoueur1)
            #CoupJ1 = strat.StrategieAgressive(_pierresJ1Depart,plateau.nbCases,plateau.nbPierresJoueur1)
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
            #CoupJ2 = strat.StrategieAgressive(_pierresJ2Depart,plateau.nbCases,plateau.nbPierresJoueur2)
            #CoupJ2 = strat.StrategieAleatoireExercice3(plateau.nbPierresJoueur2)
            CoupJ2 = strat.StrategieContreExercice3(_pierresJ2Depart,plateau.nbPierresJoueur2)
            #CoupJ2 = strat.StrategiePrudenteJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            #CoupJ2 = strat.Strategie1(15,7,plateau.nbPierresJoueur2,plateau.nbPierresJoueur1,plateau.posTroll,2)
            #CoupJ2 = strat.StrategiePrudenteNonLineaireJ2(plateau.nbPierresJoueur1,plateau.nbPierresJoueur2,plateau.nbCases,plateau.posTroll)
            CoupsReussisJ2 = 0
            for i in range(CoupJ2) :
                rand = random.uniform(0,1)
                if rand <= probaToucherJ2 :
                    CoupsReussisJ2 += 1
            CoupJ2 = CoupsReussisJ2
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