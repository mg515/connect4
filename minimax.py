import random
from copy import copy, deepcopy

class Minimax(object):

    
    stanje1 = None
    barve = [1,2]

######################################################
# konstruktor

    def __init__(self, stanje1):
        self.stanje1 = deepcopy(stanje1)

######################################################
# main funkcija objekta minimax, pove kaj je najboljša poteza za Ai in evaluira stanje boarda

    def bestMove(self, globina, stanje2, trenutni_igralec):

        if trenutni_igralec == self.barve[0]:
            nasprotni_igralec = self.barve[1]
        else:
            nasprotni_igralec = self.barve[0]

        veljavne_poteze = {} 
        for stolpec in range(7):

            if self.jeVeljavno(stolpec, stanje2):

                stanje123 = self.premakni(stanje2, stolpec, trenutni_igralec)
                veljavne_poteze[stolpec] = -self.isci(globina-1, stanje123, nasprotni_igralec)
        
        naj_v1 = -99999999
        naj_poteza = None
        poteze = list(veljavne_poteze.items())
        random.shuffle(poteze)
        for poteza, v1 in poteze:
            if v1 >= naj_v1:
                naj_v1 = v1
                naj_poteza = poteza
        
        return [naj_poteza, naj_v1]

######################################################
# pomozna funkcija za evaluacijo

    def isci(self, globina, stanje2, trenutni_igralec):
        

        veljavne_poteze = []
        for i in range(7):

            if self.jeVeljavno(i, stanje2):

                stanje123 = self.premakni(stanje2, i, trenutni_igralec)
                veljavne_poteze.append(stanje123)
        

        if globina == 0 or len(veljavne_poteze) == 0 or self.konecIgre(stanje2):

            return self.vrednostStanja(stanje2, trenutni_igralec)

        if trenutni_igralec == self.barve[0]:
            nasprotni_igralec = self.barve[1]
        else:
            nasprotni_igralec = self.barve[0]

        v1 = -99999999
        for stopnja_globje in veljavne_poteze:
            if stopnja_globje == None:
                print("error")
            v1 = max(v1, -self.isci(globina-1, stopnja_globje, nasprotni_igralec))
        return v1


######################################################
# pove, ce je poteza veljavna

    def jeVeljavno(self, col, stanje2):
        
        for i in range(6):
            if stanje2[i][col] == 0:
                return True
        

        return False

######################################################
# pogoji za konec igre
    
    def konecIgre(self, stanje2):
        if self.racunajZaporedje(stanje2, self.barve[0], 4) >= 1:
            return True
        elif self.racunajZaporedje(stanje2, self.barve[1], 4) >= 1:
            return True
        else:
            return False
        
######################################################
# update stanja

    def premakni(self, stanje2, col, barva):

        stanje123 = [x[:] for x in stanje2]
        for i in range(6):
            if stanje123[i][col] == 0:
                stanje123[i][col] = barva
                return stanje123

######################################################
# funkcija za ovrednotenje stanja iz vidika Ai igralca

    def vrednostStanja(self, stanje2, barva):


        if barva == self.barve[0]:
            n_barva = self.barve[1]
        else:
            n_barva = self.barve[0]
        
        moje_stiri = self.racunajZaporedje(stanje2, barva, 4)
        moje_tri = self.racunajZaporedje(stanje2, barva, 3)
        moje_dve = self.racunajZaporedje(stanje2, barva, 2)
        nasprotnik_stiri = self.racunajZaporedje(stanje2, n_barva, 4)
        nasprotnik_tri = self.racunajZaporedje(stanje2, n_barva, 3)
        nasprotnik_dve = self.racunajZaporedje(stanje2, n_barva, 2)

        if nasprotnik_stiri > 0:
            return -100000
        else:
            v0 = (moje_stiri*99999 + moje_tri*100 + moje_dve*10 -
                    nasprotnik_stiri*99999 - nasprotnik_tri*100 - nasprotnik_dve*10)
            return v0

######################################################
# iskanje in stetje zaporedja

    def racunajZaporedje(self, stanje2, barva, stevec3):
        stevec = 0
        for i in range(6):
            for j in range(7):
                if stanje2[i][j] == barva:
                    stevec += self.vertikalno(i, j, stanje2, stevec3)
                    stevec += self.horizontalno(i, j, stanje2, stevec3)
                    stevec += self.diagonalno(i, j, stanje2, stevec3)
        return stevec

######################################################
# vertikalen pregled zaporedij
    
    def vertikalno(self, row, stolpec, stanje2, stevec3):
        stevec1 = 0
        for i in range(row, 6):
            if stanje2[i][stolpec] == stanje2[row][stolpec]:
                stevec1 += 1
            else:
                break
    
        if stevec1 >= stevec3:
            return 1
        else:
            return 0

######################################################
# horizontalen pregled zaporedij
    
    def horizontalno(self, row, stolpec, stanje2, stevec3):
        stevec1 = 0
        for j in range(stolpec, 7):
            if stanje2[row][j] == stanje2[row][stolpec]:
                stevec1 += 1
            else:
                break

        if stevec1 >= stevec3:
            return 1
        else:
            return 0

######################################################
# diagonalen pregled zaporedij

    def diagonalno(self, row, stolpec, stanje2, stevec3):

        skupno = 0
        stevec1 = 0
        j = stolpec
        for i in range(row, 6):
            if j > 6:
                break
            elif stanje2[i][j] == stanje2[row][stolpec]:
                stevec1 += 1
            else:
                break
            j += 1 
            
        if stevec1 >= stevec3:
            skupno += 1

        stevec1 = 0
        j = stolpec
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif stanje2[i][j] == stanje2[row][stolpec]:
                stevec1 += 1
            else:
                break
            j += 1 

        if stevec1 >= stevec3:
            skupno += 1

        return skupno
