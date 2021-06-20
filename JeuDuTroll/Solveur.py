# Solveur permettant de resoudre des simplex avec un nombre de contraintes et de variables quelconques
import numpy as np
from scipy.optimize import linprog

def solve(mat) : # Fonction qui, prenant une matrice de gains en parametre, va renvoyer le resultat d'un probleme d'optimisation par un simplex.
    A = [] # Les sous-contraintes de type >=  ( tableau 2D)
    Aeq = [] # Les sous-contraintes de type = ( tableau 2D)
    B = [] # Les operandes de gauche des sous-contraintes associees a A (tableau 2D)
    Beq = np.array([1]) # Les operandes des sous-contraintes associees a Aeq. Il n'y en a qu'une seule dans notre cas (aX1 + ... + aXn = 1 ) (tableau 1D)
    C = [] # Les coefficients de la fonction objectif (tableau 1D)
    bnds = [] # les intervalles de definition
    colAeq = [] # Contient les coefficients pour la contrainte d'egalite .
    b = (0.,1.0)
    for i in range(len(mat[0])) :
        colA = []
        for j in range (len(mat)) : # Remplissage des sous-contraintes(coefficients de chaque colonne de la matrice de gains)
            colA.append(-mat[j][i]) # <= par defaut dans scipy, donc il faut prendre l'oppose
        colA.append(1)
        A.append(colA)
        B.append(0)
    for i in range (len(A[0])-1) : # Pour chaque variable, on lui affecte 1 dans la fonction de sommes et 0 dans la fonction objectif.
        colAeq.append(1)
        bnds.append(b)
        C.append(0)
    colAeq.append(0) # le gain n'est pas concerne par la contrainte d'egalite
    bnds.append((-1.0,1.0)) #bornes du gain
    C.append(-1) # par defaut, scipy minimise les fonction, donc il faut prendre l'oppose pour maximiser
    Aeq.append(colAeq)
    tmp = np.asarray(A[0])
    for i in range(1,len(A)) :
        tmp2 = np.asarray(A[i])
        tmp = np.append(tmp,tmp2)
    tmp = tmp.reshape(len(A),len(A[0])) # cast de la liste des sous-constraintes en tableau numpy.
    #print(" A : ",tmp, " B : ", B, " C : ", C, " Aeq : ",Aeq, " Beq : ", Beq)
    #print(" matrice de depart : ",mat)
    #print(len(tmp),"   ", len(tmp[0]))
    return linprog(C,A_ub=tmp,b_ub=B,A_eq=Aeq,b_eq=Beq,bounds=bnds,method="simplex")


def ValeurGainsMatrice(size_x,size_y,mat) : # retourne le dernier x de la maximisation, donc le gain
    res = solve(mat).x
    return res[len(res)-1]


def MatriceGains(nbPierresJ1, nbPierresJ2,positionTroll,nbCases,matrice) : # remplissage de la matrice de gains
    positionTrollInitiale = positionTroll - (nbCases//2 + 1 ) # 1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range (nbPierresJ1) :
        for j in range (nbPierresJ2) : # i = nb pierres restantes au J1, j = nb pierres restantes au J2
            t = positionTrollInitiale
            nbPierresLanceesJ1 = nbPierresJ1 - i
            nbPierresLanceesJ2 = nbPierresJ2 - j # pierres lancees = pierres initiales - pierres restantes, mouvement du troll en fonction.
            if nbPierresLanceesJ1 < nbPierresLanceesJ2 :
                t -= 1
            if nbPierresLanceesJ1 > nbPierresLanceesJ2 :
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
                    matrice[i][j] =  ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si les joueurs ont le même nombre de pierres, le cas est trivial si le troll est au milieu (pas d'avantage pour un joueur). Sinon, ce n'est plus un cas trivial.
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
                matrice[i][j] = ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si on n'est pas dans un cas trivial, remplissage de la matrice par un simplex de sous-matrices deja calculees.
                #print(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp))
                #print(round(SimplexGainsMatrice(len(matTmp),len(matTmp[0]),matTmp).x[len(matTmp)],10))
            #print("i = ",i," j = ",j, "t = ",t, " gain associe : ",matrice[i][j])






def MatriceGainsJoueur2(nbPierresJ1, nbPierresJ2,positionTroll,nbCases,matrice) : # equivalent a la fonction au-dessus, mais calcule les gains du joueur 2.
    positionTrollInitiale = positionTroll - (nbCases//2 + 1 ) #1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range (nbPierresJ2) :
        for j in range (nbPierresJ1) :
            t = positionTrollInitiale
            nbPierresLanceesJ1 = nbPierresJ1 - j
            nbPierresLanceesJ2 = nbPierresJ2 - i 
            if nbPierresLanceesJ1 < nbPierresLanceesJ2 :
                t -= 1
            if nbPierresLanceesJ1 > nbPierresLanceesJ2 :
                t += 1
            if t == -(nbCases//2) : 
                matrice[i][j] = 1
            elif t == (nbCases//2)-1 :
                matrice[i][j] = -1
            elif i == 0 :
                if t < 0 :
                    if j == abs(t) :
                        matrice[i][j] = 0
                    elif j > abs(t) :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t > 0 :
                    matrice[i][j] = -1
                else :
                    if j == 0 :
                        matrice[i][j] = 0
                    else :
                        matrice[i][j] = -1
            elif j == 0 : 
                if t > 0 :
                    if i == t :
                        matrice[i][j] = 0
                    elif i < t :
                        matrice[i][j] = -1
                    else :
                        matrice[i][j] = 1
                elif t < 0 :
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
                    matrice[i][j] = ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp)
            else :
                matTmp = []
                for iTmp in range(i):
                    col = []
                    for jTmp in range(j):
                        col.append(matrice[iTmp][jTmp])
                    matTmp.append(col)
                matrice[i][j] = ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp) # si on n'est pas dans un cas trivial, remplissage de la matrice par un simplex de sous-matrices deja calculees.





def Debug(x=15,y=15,troll=4,cases=7) : # Executions de debogage, permet de voir les distributions de probabilite a partir d'une matrice

    matrice = []
    for i in range(x) :
        col = []
        for j in range(y) :
            col.append(float("inf"))
        matrice.append(col)

    MatriceGains(x,y,troll,cases,matrice)
    print(solve(matrice))
    for i in range(len(matrice)) :
        print(matrice[i])


#Debug(5,4,2,5)