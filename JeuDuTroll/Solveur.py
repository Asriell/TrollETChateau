import numpy as np
from scipy.optimize import minimize

class Solveur:
    x0 = [0,0,0,0,1]
    bnds = ((0,1),(0,1),(0,1),(0,1))
    cons = []
    def Objective(x) :
            return
    objective = Objective
    def __init__(self, _x0=[0,0,0,0,1], _bnds = ((0,1),(0,1),(0,1),(0,1)), _objective = Objective, _cons = []):
        self.x0 = _x0
        self.bnds = _bnds
        self.objective = _objective
        self.cons = _cons




    def solve(self) :
        sol = minimize(self.objective,self.x0,method='SLSQP',bounds = self.bnds,constraints = self.cons)
        return sol




g = [
        [31/6,-1,-2,-3],
        [-1,31/6,-1,-2],
        [-2,-1,31/6,-1],
        [-3,-2,-1,31/6]
        ]

nbVariables = 4

def ObjectiveN(n):
    def Objective(x) : #x = max (x1+x2+...+xN+g) = min (- (x1+x2+...+xN+g) ) et mettre x1 à xN à 0 et g à 1
        sum = 0
        for k in range(n):
            sum += x[k]
        return -sum
    return Objective


def Objective(x) : #x = max (x1+x2+...+xN+g) = min (- (x1+x2+...+xN+g) ) et mettre x1 à xN à 0 et g à 1
    sum = 0
    for k in range(nbVariables+1):
        sum += x[k]
    return -sum

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


def constraintSumN(n):
    def constraintSum(x) :
        sum = -1
        for k in range(n):
            sum+= x[k]
        return sum
    return constraintSum

def constraints(n,gains,vars):
    def constraintN(x) :
        sum = 0
        for k in range(0,vars,1):
            sum += gains[k][n] * x[k]
        return sum - x[vars]
    return constraintN




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


def SimplexGainsMatrice(size_x,size_y,mat) :
    full = True
    for i in range(size_x):
        for j in range(size_y) :
            if (mat[i][j] == float("inf")) :
                full = False
    assert(full)
    b = (0.0,1.0)
    bnds = []
    x0 = []
    for k in range(size_x):
        bnds.append(b)
        x0.append(0)
    bnds.append((-1.0,1.0)) #bornes du gain
    x0.append(1) #pour le gain
    bnds = tuple(bnds)
    cons = []
    for k in range(size_y) :
        cons.append({'type' : 'ineq', 'fun' : constraints(k,mat,size_x)})
    conSum = {'type' : 'eq', 'fun' : constraintSumN(size_x)}
    cons.append(conSum)
    solveur = Solveur(_x0=x0,_bnds=bnds,_objective = ObjectiveN(size_x),_cons=cons)
    return solveur.solve()

def ValeurGainsMatrice(size_x,size_y,mat) :
    #return SimplexGainsMatrice(size_x,size_y,mat).x[size_x]
    return SimplexGainsMatrice(size_x,size_y,mat).fun

def MatriceGains(NbPierresJ1,nbPierresJ2,PositionTroll,nbCases,mat):
    t = PositionTroll - (nbCases//2 + 1 ) #1 = -3 = Chez le J1, 4 = 0 = Au Milieu, 7 = 3 = Chez le J2 Pour nbCases = 7
    for i in range(NbPierresJ1) :
        for j in range(nbPierresJ2) :
            if i == j and t == 0 :
                mat[i][j] = 0
            elif i == 0 :
                if j == abs(t) :
                    mat[i][j] = 0
                elif j < abs(t) :
                    mat[i][j] = 1
                else :
                    mat[i][j] = -1
            elif j == 0 :
                if i == abs(t) :
                    mat[i][j] = 0
                elif i < abs(t) :
                    mat[i][j] = -1
                else :
                    mat[i][j] = 1
            else :
                mat[i][j] = ValeurGainsMatrice(i-1,j-1,mat)


