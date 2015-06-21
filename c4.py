from tkinter import *
import random
import time
import tkinter.messagebox
from copy import copy, deepcopy
from minimax import Minimax
import tkinter.simpledialog
import math

######################################################
# konstruktor

class Igra(Tk):
    def __init__(self):
        Tk.__init__(self)
        menu = Menu(self)
        self.boind = False
        menu.add_command(label="New Game", command=self.novaigra)
        menu.add_command(label="BestOf10", command=self.bo10)
        menu.add_command(label="Difficulty", command=self.izberitezavnost)
        menu.add_command(label="Quit", command=self.koncaj)
        self.config(menu=menu)
        self.platno=Canvas(self, width=705, height=605)
        self.platno.grid(row=1, column=1, columnspan=7)
        self.platno.bind("<Button-1>", self.klik)
        self.playerscore = 0
        self.aiscore = 0
        self.neodloceno = 0
        self.tezavnost=4
        self.zacetek()

        self.mainloop()

######################################################
# funkcija za oznacevanje rezultata in izbiro tezavnosti

    def rezultat(self):
        self.labelp = Label(self, text=("Igralec: " + str(self.playerscore)))
        self.labelp.grid(row=2, column=1)
        self.labelai = Label(self, text=("HAL9000: " + str(self.aiscore)))
        self.labelai.grid(row=2, column=2)
        self.labelai = Label(self, text=("Neodloceno: " + str(self.neodloceno)))
        self.labelai.grid(row=2, column=3)

    def izberitezavnost(self):
        self.tezavnost = tkinter.simpledialog.askinteger(
            "Choose Difficulty", "Choose between 1 and 5",
            initialvalue=self.tezavnost, minvalue=1, maxvalue=5)
        self.zacetek()
        


        

######################################################
# funkcija za gumbe nova igra, koncaj in bo10

    def novaigra(self):
        self.aiscore += 1
        m1=tkinter.messagebox.askyesno("You sure","New Game?")
        if m1:
            self.zacetek()
        else:
            return

    def koncaj(self):
        quit()

    def bo10(self):
        tkinter.messagebox.showinfo("BO10", "You have started the BestOf 10 mode. Good luck!")
        self.aiscore=0
        self.playerscore=0
        self.neodloceno=0
        self.zacetek()
        self.boind = True

            
######################################################
# konstrukcija zacetnega stanja

    def zacetek(self):
        if self.boind and self.aiscore+self.neodloceno+self.playerscore==10:
            if self.playerscore == self.aiscore:
                tkinter.messagebox.showinfo("Tie", "It's a tie!")
            if self.playerscore > self.aiscore:
                tkinter.messagebox.showinfo("You win!", "GG, You win!")
            if self.aiscore > self.playerscore:
                tkinter.messagebox.showinfo("ai stronk", "Ai too strong?")
                
        self.platno.delete(ALL)
        self.platno.configure(background='white')
        for i in range(1,6):
            self.platno.create_line(3, i*100+3, 700+3, i*100+3, width=2, fill="lightgray")
        for i in range(0,7):
            self.platno.create_line(i*100+3, 4, i*100+3, 600+3, width=2, fill="lightgray")
        self.platno.create_line(3, 3, 703, 3, width=2, fill="black") #1
        self.platno.create_line(3, 3, 3, 603, width=2, fill="black") #4
        self.platno.create_line(3, 603, 703, 603, width=2, fill="black") #2
        self.platno.create_line(703, 3, 703, 603, width=2, fill="black") #3


        self.stanje=[[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0],
                     [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0],
                     [0,0,0,0,0,0]]
        self.rezultat()
        self.prosti = [0,1,2,3,4,5,6]
        self.steviloklikov = [0,0,0,0,0,0,0]
        a = random.randint(1,2)
        if a==1:
            self.platno.bind("<Button-1>", self.brezveze)
            self.randomai(-1)
        else:
            self.platno.bind("<Button-1>", self.klik)
        
######################################################
# funkcija za klik na platno (po koordinatah)
        
    def klik(self, event):
        x=event.x
        if x < 100:
            self.f1(0)
        elif x < 200:
            self.f1(1)
        elif x < 300:
            self.f1(2)
        elif x < 400:
            self.f1(3)
        elif x < 500:
            self.f1(4)
        elif x < 600:
            self.f1(5)
        else:
            self.f1(6)


######################################################
# funkcija za akcijo cloveskega igralca

    def f1(self,a):
        self.platno.bind("<Button-1>", self.brezveze)
        v = [i for i in range(len(self.stanje[a][:])) if self.stanje[a][i]!=0]
        v.append(6)
        m = min(v)-1
        if self.steviloklikov[a] == 6:
            self.platno.bind("<Button-1>", self.klik)
        else:
            self.stanje[a][m] = 1
            self.steviloklikov[a] += 1
            self.risanje(1, a, m)
                
            if self.zmaga(self.stanje):
                self.playerscore += 1
                self.risanjezmaga()
                m1=tkinter.messagebox.askyesno("Congratz","You win! New game?")
                if m1:
                    self.zacetek()
                    return
                else:
                    quit()
                
            if sum(self.steviloklikov)==42:
                self.neodloceno+=1
                m1=tkinter.messagebox.askyesno("Tie!","It's a tie! New game?")
                if m1:
                    self.zacetek()
                    return
                else:
                    quit()
               
            else:
                self.randomai(-1)


######################################################
# funkcija za akcijo ai igralca

    def randomai(self, r):
        print("---------------")
        g = deepcopy(self.stanje)
        g = transponiraj(g)
        g = obrni(g)
        m = Minimax(g)
        p = m.bestMove(self.tezavnost, g, 2)[0]
        if self.preverjanje1(self.stanje)[0] != -1 or self.preverjanje1(self.stanje)[1] != -1:
            if self.preverjanje1(self.stanje)[0] != -1:
                p = self.preverjanje1(self.stanje)[0]
            else: p = self.preverjanje1(self.stanje)[1]
            
        v = [i for i in range(len(self.stanje[p][:])) if self.stanje[p][i]!=0]
        v.append(6)
        m = min(v)-1


        self.steviloklikov[p] += 1
        self.stanje[p][m] = 2
        self.risanje(2, p, m)
        self.platno.bind("<Button-1>", self.klik)


        if self.zmaga(self.stanje):
            self.aiscore += 1
            self.risanjezmaga()
            m1=tkinter.messagebox.askyesno("Jaesus","You lost! New game?")
            if m1:
                self.zacetek()
                return
            else:
                return

        if sum(self.steviloklikov)==42:
            self.neodloceno+=1
            m1=tkinter.messagebox.askyesno("Tie","It's a tie. New game?")
            if m1:
                self.zacetek()
                return
            else:
                quit()


                
            
######################################################
# pogoji za zmago                

    def zmaga(self, stanjee):
        for i in range(0, 6):
            for j in range(0, 4):
                if (stanjee[j][i]==stanjee[j+1][i]==stanjee[j+2][i]==stanjee[j+3][i]
                and stanjee[j][i]!=0 and stanjee[j+1][i]!= 0 and stanjee[j+2][i]!=0 and stanjee[j+3][i]!=0):
                    self.zmagovalnapoteza = [j*100+15, i*100+50, (j+4)*100-15, i*100+50, self.radiani(90)]
                    return True
        for i in range(0, 7):
            for j in range(0, 3):
                if (stanjee[i][j]==stanjee[i][j+1]==stanjee[i][j+2]==stanjee[i][j+3]
                and stanjee[i][j]!=0 and stanjee[i][j+1]!= 0 and stanjee[i][j+2]!=0 and stanjee[i][j+3]!=0):
                    self.zmagovalnapoteza = [i*100+53, j*100+15, i*100+53, (j+4)*100-15, self.radiani(0)]
                    return True
        for i in range(0, 4):
            for j in range(3, 6):
                if (stanjee[i][j]==stanjee[i+1][j-1]==stanjee[i+2][j-2]==stanjee[i+3][j-3]
                and stanjee[i][j]!=0 and stanjee[i+1][j-1]!= 0 and stanjee[i+2][j-2]!=0 and stanjee[i+3][j-3]!=0):
                    self.zmagovalnapoteza = [i*100+15, j*100+90, (i+4)*100-15, (j-4)*100+120, self.radiani(180-45)]
                    return True

        for i in range(0, 4):
            for j in range(0, 3):
                if (stanjee[i][j]==stanjee[i+1][j+1]==stanjee[i+2][j+2]==stanjee[i+3][j+3]
                and stanjee[i][j]!=0 and stanjee[i+1][j+1]!= 0 and stanjee[i+2][j+2]!=0 and stanjee[i+3][j+3]!=0):
                    self.zmagovalnapoteza = [i*100+15, j*100+15, (i+4)*100-15, (j+4)*100-15, self.radiani(45)]
                    return True


######################################################
# preverjanje pogojev za zmago poraz eno potezo naprej, zgolj varnostno, ostale izracune opravlja klic funkcije bestMove

    def preverjanje1(self, stanjee):
        zmaga = -1
        poraz = -1
        for p in self.prosti:
            stanje1 = deepcopy(stanjee)
            v = [i for i in range(len(stanje1[p][:])) if stanje1[p][i]!=0]
            v.append(6)
            m = min(v)-1
            if self.steviloklikov[p] != 6:
                stanje1[p][m] = 2
                if self.zmaga(stanje1):
                    zmaga = p

        for p in self.prosti:
            stanje1 = deepcopy(stanjee)
            v = [i for i in range(len(stanje1[p][:])) if stanje1[p][i]!=0]
            v.append(6)
            m = min(v)-1
            if self.steviloklikov[p] != 6:
                stanje1[p][m] = 1
                if self.zmaga(stanje1):
                    poraz = p
        return [zmaga, poraz]



######################################################
# brezveze
    
    def brezveze(self, event):
        pass


######################################################
# risanje krogcev, kot parameter sprejme barvo krogca, stolpec in vrstico


    def risanje(self, igralec, p, m):
        if igralec==1:
            barva="steel blue"
        else: barva="chocolate"
        r = deepcopy(self.stanje)
        r = transponiraj(r)
        r = obrni(r)
        minimax1 = Minimax(r)
        s = minimax1.vrednostStanja(r, igralec)
        print(s)
        v = 6
        g=self.platno.create_rectangle(100*p+v, v, 100+100*p-1, 100-1, fill=barva, outline="white")
        for i in range(0, m*100):
            self.platno.move(g, 0, 1)
            self.platno.update()
            time.sleep(1/(50*i+5))


######################################################
# risanje zmagovalne crte

    def risanjezmaga(self):
        d = self.dolzina(self.zmagovalnapoteza[0], self.zmagovalnapoteza[1],
                         self.zmagovalnapoteza[2], self.zmagovalnapoteza[3])
        
        kd = 0
        for i in range(1, 101):
            kd += d/100
            c = self.platno.create_line(self.zmagovalnapoteza[0], self.zmagovalnapoteza[1],
                                        self.polarne(self.zmagovalnapoteza[4], kd, "x") + self.zmagovalnapoteza[0],
                                        self.polarne(self.zmagovalnapoteza[4], kd, "y") + self.zmagovalnapoteza[1],
                                        width=3, fill="black")
            self.platno.update()
            time.sleep(0.005)


######################################################
# nekaj pomoznih funkcij (uporabljene znotraj funkcije risanjezmaga
    def polarne(self, fi, d, tip):
        if tip == "x":
            pol = d*math.sin(fi)
        else: pol = d*math.cos(fi)
        return pol

    def dolzina(self, x1, y1, x2, y2):
        return ((x2-x1)**2+(y2-y1)**2)**(1/2)

    def radiani(self, kot):
        return math.pi*(1/180)*kot


        
######################################################
# dve zunanji funkciji 
        
def transponiraj(mat):
    m, n = len(mat), len(mat[0])
    return [[mat[i][j] for i in range(m)] for j in range(n)]

def obrni(mat):
    return mat[::-1]


Igra()
