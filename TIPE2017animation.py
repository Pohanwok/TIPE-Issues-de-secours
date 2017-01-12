import numpy as np
import random
from tkinter import *

contraste=999
epaisseur=7
r2=1.414
vitesseMax=1.34 #m.s^(-1)

def creerSalle(x=13,y=10):
    Salle=np.zeros((x+2,y+2))
    for i in range(x+2):
        Salle[i,0]=-1
        Salle[i,y+1]=-1
    for j in range(y+2):
        Salle[0,j]=-1
        Salle[x+1,j]=-1
    return Salle

def placerObstacle(M,x1,y1,x2,y2):
    """x1<=x2 et y1<=y2 sont les abcisses et ordonées des obstacles rectangulaires"""
    D=np.array([i[:] for i in M])
    for i in range(x2-x1+1):
        for j in range(y2-y1+1):
            D[x1+i,y1+j]=-1
    return D

Salle=creerSalle(100,100)

Salle=placerObstacle(Salle,13,10,25,33)
Salle=placerObstacle(Salle,31,24,42,38)
Salle=placerObstacle(Salle,4,38,15,23)

Salle=placerObstacle(Salle,13,55,84,88)
Salle=placerObstacle(Salle,49,9,59,52)
Salle=placerObstacle(Salle,72,12,94,39)

Ssalle=[[24,0],[25,0],[26,0]]

def Affichage(M=Salle, S=Ssalle):
    n,m=M.shape
    fenetre=Tk()
    fenetre.title('Affichage Distance')
    csalle= Canvas(fenetre, height=n*epaisseur, width=m*epaisseur, background='grey')
    CaseAcceptable=[]
    D,V=PPVdistance(M,S)
    global D,V

    dmax=-1
    for i in range(n):
        for j in range(m):
            if D[i,j]>=dmax:
                dmax=D[i,j]

    for i in range(0,n*epaisseur,epaisseur):
        for j in range(0,m*epaisseur,epaisseur):
            if [i//epaisseur,j//epaisseur] in S:
                issue=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='green',outline='black')
                csalle.tag_bind(issue, '<Button-1>', Click)
                
                
            elif D[i//epaisseur,j//epaisseur]==-1:
                r=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='grey',outline='black', width=0)
                csalle.tag_bind(r, '<Button-1>', Click)  

            else:
                greenRatio=str(int(contraste-contraste*D[i//epaisseur,j//epaisseur]//dmax))
                while len(greenRatio)<3:
                    greenRatio='0'+greenRatio
                    
                r=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='#'+str(contraste)+greenRatio+'000',outline='black',width=1,activefill='grey')
                csalle.tag_bind(r, '<Button-1>', Click)
                CaseAcceptable.append([i//epaisseur,j//epaisseur])

    numAleatoire=random.randint(0,len(CaseAcceptable)-1)
    x0,y0=CaseAcceptable[numAleatoire]
    global personneX
    personneX=x0 #+random.randint(0,epaisseur-epaisseur//2)
    global personneY
    personneY=y0 #+random.randint(0,epaisseur-epaisseur//2)
    personne=csalle.create_oval(personneY,personneX,personneY+epaisseur,personneX+epaisseur, fill='blue')
    csalle.pack()

    def deplacement():
        global personneX
        global personneY
        print(personneX,personneY)
        personneX,personneY=V[personneX,personneY]
        csalle.coords(personne,personneY*epaisseur,personneX*epaisseur,personneY*epaisseur+epaisseur,personneX*epaisseur+epaisseur)
        if [personneX,personneY] not in S:
            fenetre.after(100,deplacement)

    deplacement()
    
    fenetre.mainloop()    

fenetreGenere=False

def placementObstacle(M=Salle, S=Ssalle):
    n,m=M.shape
    global fenetreGenere
    if fenetreGenere==False :
        global fenetre
        fenetre=Tk()
        fenetre.title('Placement Obstacle')
        fenetreGenere=True
        csalle= Canvas(fenetre, height=n*epaisseur, width=m*epaisseur, background='grey')
        global csalle
    D=PPVdistance(M,S)[0]
    
    dmax=-1
    for i in range(n):
        for j in range(m):
            if D[i,j]>=dmax:
                dmax=D[i,j]
    
    for i in range(0,n*epaisseur,epaisseur):
        for j in range(0,m*epaisseur,epaisseur):
            if [i//epaisseur,j//epaisseur] in S:
                issue=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='green',outline='black')
                csalle.tag_bind(issue, '<Button-1>', Click)
                
                
            elif M[i//epaisseur,j//epaisseur]==-1:
                r=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='grey',outline='black', width=0)
                csalle.tag_bind(r, '<Button-1>', Click)  

            else:
                greenRatio=str(int(contraste-contraste*D[i//epaisseur,j//epaisseur]//dmax))
                while len(greenRatio)<3:
                    greenRatio='0'+greenRatio
                    
                r=csalle.create_rectangle(j,i,j+epaisseur,i+epaisseur,fill='#'+str(contraste)+greenRatio+'000',outline='black',width=1,activefill='grey')
                csalle.tag_bind(r, '<Button-1>', Click)
    
    csalle.pack()

    def placement():
        global Obstacle
        global ex1,ey1,ex2,ey2
        global M
        if Obstacle:
            Obstacle=False
            M=placerObstacle(Salle,ex1,ex2,ey1,ey2)
            ex1,ey1,ex2,ey2=-1,-1,-1,-1
            placementObstacle(M,S)
        fenetre.after(100,placement)
            
    placement()
    
    fenetre.mainloop()    


class personnage:
    def __init__(self):
        self.x0,self.y0=CaseAcceptable[numAleatoire]
        self.x=x0+random.randint(0,epaisseur-epaisseur//2)
        self.y=y0+random.randint(0,epaisseur-epaisseur//2)

    def deplacement(self,Norme,direction):
        self.x=direction[0]-self.x
        self.y=direction[1]-self.y



ex1,ey1,ex2,ey2=-1,-1,-1,-1
Obstacle=False

def Click(event):
    global ex1,ey1,ex2,ey2
    global Obstacle
    if ex1==-1:
        ex1=event.y//epaisseur
        ey1=event.x//epaisseur
    else:
        ex2=event.y//epaisseur
        ey2=event.x//epaisseur
    if ex2!=-1:
        print('('+str(ex1)+','+str(ey1)+') , ('+str(ex2)+','+str(ey2)+')' )
        Obstacle=True

def PPVdistance(M,Sorties):
    """M est la matrice de la salle avec des -1 autour et des -1 pour les obstacles
    Sorties est la listes des coordonnées (x,y) des cases de distance 0
    Fast Marching
    D est la distance à une sortie, V est la case à prendre pour fuir ou (-1,-1) pour les obstacles et cases bloquées"""
    n,m=len(M),len(M[0])
    D=np.array([[ -1 for j in range(m)] for i in range(n)])
    V=[ [ (-1,-1) for j in range(m) ] for i in range(n) ]
    penombre=[]
    for s in Sorties:
        sx,sy=s
        penombre.append([sx, sy, 0, sx, sy])
    while len(penombre) > 0 :
        #recherche de la case de la penombre la plus proche de la sortie
        mini,i_mini=penombre[0][2],0
        for p in range(len(penombre)):
            distance = penombre[p][2]
            if distance < mini :
                mini,i_mini=distance,p
        case=penombre.pop(i_mini)
        x,y,d,vx,vy=case[0],case[1],case[2],case[3],case[4]
        D[x][y]=d
        #ajout de ses voisins non éclairés dans la file
        if (x+1 < n) and ( D[x+1][y] == -1 ) and ( M[x+1][y] == 0 ):
            penombre.append( [x+1, y, d+1, x, y] )
            D[x+1][y] = 0.5
        if (-1 < x-1) and ( D[x-1][y] == -1 ) and ( M[x-1][y] == 0 ):
            penombre.append( [x-1, y, d+1 ,x ,y] )
            D[x-1][y] = 0.5
            
        if (y+1 < m) and ( D[x][y+1] == -1 ) and ( M[x][y+1] == 0 ):
            penombre.append( [x, y+1, d+1 ,x, y] )
            D[x][y+1] = 0.5
            
        if (-1 < y-1) and ( D[x][y-1] == -1 ) and ( M[x][y-1] == 0 ):
            penombre.append( [x, y-1, d+1 ,x, y] )
            D[x][y-1] = 0.5

        if (x+1 < n) and (y+1 < m) and ( D[x+1][y+1] == -1 ) and ( M[x+1][y+1] == 0 ):
            penombre.append( [x+1, y+1, d+r2 ,x, y] )
            D[x+1][y+1] = 0.5

        if (x+1 < n) and (-1 < y-1) and ( D[x+1][y-1] == -1 ) and ( M[x+1][y-1] == 0 ):
            penombre.append( [x+1, y-1, d+r2 ,x, y] )
            D[x+1][y-1] = 0.5

        if (-1 < x-1) and (-1 < y-1) and ( D[x-1][y-1] == -1 ) and ( M[x-1][y-1] == 0 ):
            penombre.append( [x-1, y-1, d+r2 ,x, y] )
            D[x-1][y-1] = 0.5

        if (-1 < x-1) and (y+1 < m) and ( D[x-1][y+1] == -1 ) and ( M[x-1][y+1] == 0 ):
            penombre.append( [x-1, y+1, d+r2 ,x, y] )
            D[x-1][y+1] = 0.5
        V[x][y]=(vx,vy)

    return D,np.array(V)
