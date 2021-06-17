# Solveur permettant de resoudre des simplex avec un nombre de contraintes et de variables quelconques
import numpy as np
from scipy.optimize import minimize

class Solveur: # classe qui contient l'ensemble des fonctions  (objectif et sous-contraintes), sous forme de references sur fonction, ainsi que la methode de resolution.
    x0 = [0,0,0,0,1] # variables du programme lineaire par defaut.
    bnds = ((0,1),(0,1),(0,1),(0,1)) # intervalle dans lequel doivent se retrouver les variables par defaut
    cons = [] # tableau des sous-contraintes
    def Objective(x) :
            return
    objective = Objective # une fonction objectif "bidon" par defaut
    def __init__(self, _x0=[0,0,0,0,1], _bnds = ((0,1),(0,1),(0,1),(0,1)), _objective = Objective, _cons = []):
        self.x0 = _x0
        self.bnds = _bnds
        self.objective = _objective
        self.cons = _cons




    def solve(self) : # resolution du simplex
        sol = minimize(self.objective,self.x0,method='SLSQP',bounds = self.bnds,constraints = self.cons)
        return sol






def ObjectiveN(n): # fonction qui genere une fonction objectif de type x1 + x2 + ... xn.
    def Objective(x) : #x = max (x1+x2+...+xN+g) = min (- (x1+x2+...+xN+g) ) et mettre x1 à xN à 0 et g à 1
        sum = 0
        for k in range(n):
            sum += x[k]
        return -sum
    return Objective


def Objective(x) : #Un exemple de fonction objectif.
    sum = 0
    for k in range(nbVariables+1):
        sum += x[k]
    return -sum

# Des exemple de sous-contraintes
def constraint1(x) : 
    sum = 0
    for k in range(0,nbVariables,1):
        sum += g[0][k] * x[k]
    return sum - x[nbVariables]

def constraint2(x) : 
    sum = 0
    for k in range(0,nbVariables,1):
        sum += g[1][k] * x[k]
    return sum - x[nbVariables]

def constraint3(x) : 
    sum = 0
    for k in range(0,nbVariables,1):
        sum += g[2][k] * x[k]
    return sum - x[nbVariables]

def constraint4(x) : 
    sum = 0
    for k in range(0,nbVariables,1):
        sum += g[3][k] * x[k]
    return sum - x[nbVariables]

def constraintSum(x) :
    sum = -1
    for k in range(nbVariables):
        sum+= x[k]
    return sum


def constraintSumN(n): #fonction qui genere une fonction de sous-contraintes tel que x1 + x2 + ... + xn = 1
    def constraintSum(x) :
        sum = -1 # equivalent a x1 + x2 + ... + xn - 1 = 0
        for k in range(n):
            sum+= x[k]
        return sum
    return constraintSum

def constraints(n,gains,vars): #fonction qui genere une fonction de sous-contraintes telle que gains(1,n) * x1 + gains(2,n) * x2 + ... + gains(vars-1,n) * x(vars-1) - xvars  <= 0 (le dernier x etant g)
    def constraintN(x) :
        sum = 0
        for k in range(0,vars,1):
            sum += gains[k][n] * x[k]
        return sum - x[vars]
    return constraintN



# Des exemples d'utilisation des fonctions de contraintes et d'objectif : 
g = [
        [31/6,-1,-2,-3],
        [-1,31/6,-1,-2],
        [-2,-1,31/6,-1],
        [-3,-2,-1,31/6]
        ]

nbVariables = 4

def Example() :
    b = (0.0,1.0)
    bnds = []
    for k in range(nbVariables+1):
        bnds.append(b)
    bnds = tuple(bnds)

    con1 = {'type' : 'ineq', 'fun' : constraint1}
    con2 = {'type' : 'ineq', 'fun' : constraint2}
    con3 = {'type' : 'ineq', 'fun' : constraint3}
    con4 = {'type' : 'ineq', 'fun' : constraint4}
    conSum = {'type' : 'eq', 'fun' : constraintSum}
    cons = [con1, con2,con3,con4,conSum]
    solveur = Solveur(_x0=[0,0,0,0,1],_bnds=bnds,_objective = Objective,_cons=cons)
    print(solveur.solve())

def Example2() :
    b = (0.0,1.0)
    bnds = []
    for k in range(nbVariables+1):
        bnds.append(b)
    bnds = tuple(bnds)
    cons = []
    for k in range(4) :
        cons.append({'type' : 'ineq', 'fun' : constraints(k,g,4)})
    conSum = {'type' : 'eq', 'fun' : constraintSum}
    cons.append(conSum)
    solveur = Solveur(_x0=[0,0,0,0,1],_bnds=bnds,_objective = Objective,_cons=cons)
    print(solveur.solve())




def SimplexGainsMatrice(size_x,size_y,mat) : # Calcul d'un simplex pour une matrice mat(size_x,size_y)
    full = True
    for i in range(size_x):
        for j in range(size_y) :
            if (mat[i][j] == float("inf")) : # valeur infinie = valeur non calculee dans la matrice
                full = False
    if not full : # matrice initialisee par des valeurs infinies, on verifie qu'il n'y ait pas de trous dans la matrice (sinon, simplex impossible)
        for i in range (len(mat)) :
            print(mat[i])
    assert full,"valeurs non calculees dans la matrice : " # Si il y a des valeurs non calculees dans la matrice, inutile d'aller plus loin.
    b = (0.0,1.0) # bornes des variables a maximiser
    bnds = []
    x0 = []
    for k in range(size_x): # pour chaque variable, on ajoute son intervalle, et chaque variable vaut 0 dans la fonction objectif (on cherche a maximiser g)
        bnds.append(b)
        x0.append(0)
    bnds.append((-1.0,1.0)) #bornes du gain
    x0.append(1) #pour le gain
    bnds = tuple(bnds)
    cons = []
    for k in range(size_y) : # chaque contrainte correspond a une colonne de la matrice
        cons.append({'type' : 'ineq', 'fun' : constraints(k,mat,size_x)})
    conSum = {'type' : 'eq', 'fun' : constraintSumN(size_x)} # ajout de la contrainte de somme
    cons.append(conSum)
    solveur = Solveur(_x0=x0,_bnds=bnds,_objective = ObjectiveN(size_x),_cons=cons)
    return solveur.solve() # On resout le simplex

def ValeurGainsMatrice(size_x,size_y,mat) : # retourne le dernier x de la maximisation, donc le gain
    return SimplexGainsMatrice(size_x,size_y,mat).x[size_x]


def MatriceGains(nbPierresJ1, nbPierresJ2,positionTroll,nbCases,matrice) : # remplissage de la matrice de gains
    positionTrollInitiale = positionTroll - (nbCases//2 + 1 ) #1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range (nbPierresJ1) :
        for j in range (nbPierresJ2) : # i = nb pierres restantes au J1, j = nb pierres restantes au J2
            t = positionTrollInitiale
            nbPierresLanceesJ1 = nbPierresJ1 - i
            nbPierresLanceesJ2 = nbPierresJ2 - j # pierres lancees = pierres initiales - pierres restantes, mouvement du troll en fonction.
            if nbPierresLanceesJ1 < nbPierresLanceesJ2 :
                t -= 1
            if nbPierresLanceesJ1 > nbPierresLanceesJ2 :
                t += 1
            if t == -((nbCases//2) - 1) :
                matrice[i][j] = -1
            elif t == (nbCases//2)-1 :
                matrice[i][j] = 1
            if i == 0 : # remplissage de la matrice pour tous les cas triviaux
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
            elif j == 0 :
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
            else :
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
                #print(ValeurGainsMatrice(len(matTmp),len(matTmp[0]),matTmp))


#matrice = []
#for i in range(20) :
#    col = []
#    for j in range(21) :
#        col.append(float("inf"))
#    matrice.append(col)

#MatriceGains(20,20,3,7,matrice)
#print(SimplexGainsMatrice(20,20,matrice))

#matTmp = []
#for iTmp in range(15):
#    col = []
#    for jTmp in range(15):
#        col.append(matrice[iTmp][jTmp])
#    matTmp.append(col)

#for i in range(len(matTmp)) :
#    print(matTmp[i])

#print(SimplexGainsMatrice(9,2,matTmp))

#matrice = [
#        [31/6,-1,-2,-3],
#        [-1,31/6,-1,-2],
#        [-2,-1,31/6,-1],
#        [-3,-2,-1,31/6]
#        ]

#print(SimplexGainsMatrice(4,4,matrice))