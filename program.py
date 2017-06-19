import re
import math
import sys
## \brief Wektory w układzie kartezjańskim
# \author Bernadeta Nowosielska
# \param x,y,z wspołrzędne w układzie karteziańskim
class vector:
    x=0
    y=0
    z=0
    ## \brief Konstuktor 
    # \param a,b,c pobierane współrzędne
    def __init__(__self__,a,b,c):
        __self__.x=a
        __self__.y=b
        __self__.z=c
    ## \brief Długość wektora	
    # \return długość wekotora
    def leng (__self__):
        return math.sqrt(__self__.x*__self__.x + __self__.y*__self__.y + __self__.z*__self__.z )
    ## \brief Iloczyn wektorowy
	# \param p atom lub wektor
    # \return obiekt klasy wektor 
    def vector_prod(__self__,p):
        w=vector(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    ## \brief Iloczyn skalarny
    # \param p atom lub wektor
    # \return wynik iloczynu skalarnego
    def scalar_prod(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    ## \brief Pozwala na wydrukowanie wektora
    def __str__(__self__):
        return "[ "+str(__self__.x) + ", "+str(__self__.y) + ", "+str(__self__.z) + "]"
## \brief Atomy 
# \author Bernadeta Nowosielska
# \param x,y,z współrzędne w układzie kartezjanskim
# \param ID unikalny identyfikator
# \param element pierwiastek chemiczny
# \param znacznik atomy "funkcyjne"
class atom:
    x=0
    y=0
    z=0
    ID=""
    element=""
    znacznik=""
    def __init__(__self__,a,b,c,ID,element, znacznik):
        __self__.x=a
        __self__.y=b
        __self__.z=c
        __self__.ID=ID
        __self__.element=element
        __self__.znacznik=znacznik	
    def scalar_prod(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    def rotate(__self__,m):
        x=__self__.x
        y=__self__.y
        z=__self__.z
        __self__.x=x*m[0][0]+y*m[0][1]+z*m[0][2]
        __self__.y=x*m[1][0]+y*m[1][1]+z*m[1][2]
        __self__.z=x*m[2][0]+y*m[2][1]+z*m[2][2]
    def translation(__self__,v):
        __self__.x+=v.x
        __self__.y+=v.y
        __self__.z+=v.z
    def vector_prod(__self__,p):
        w=vector(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    def __str__(__self__):
        return ( '%6s %2s %7.4f %7.4f %7.4f %6s' %(__self__.ID,__self__.element, __self__.x,__self__.y,__self__.z, __self__.znacznik))
## \brief Monomery
# \author Bernadeta Nowosielska
# \param ID nazwa monomeru
# \param number_of_atoms liczba atomów w monomerze
# \param number_of_bonds liczba wiązań w monomerze
class monomer:
    ID=""
    number_of_atoms = 0
    number_of_bonds = 0
    ## \brief Konstuktor
	# \param ID nazwa
	# \param noa liczba atomów w monomerze
    # \param atoms tablica zawierająca obiekty klasy atom
	# \param nob liczba wiązań w monomerze
	# \param bonds tablica wiązań
	# \param wazne_atomy tablica atomów funkcyjnych
    def __init__(__self__,ID,noa, atoms, nob, bonds, wazne_atomy):
        __self__.atoms= []
        __self__.bonds= []
        __self__.wazne_atomy=[]
        for i in range(len(wazne_atomy)):
            __self__.wazne_atomy.append(wazne_atomy[i])
        for i in range (nob):
            __self__.bonds.append(bonds[i])
        __self__.ID=ID
        __self__.number_of_atoms=noa
        __self__.number_of_bonds=nob
        for i in range (noa):
            x=atoms[i].x
            y=atoms[i].y 
            z=atoms[i].z
            ID=atoms[i].ID
            element=atoms[i].element
            znacznik=atoms[i].znacznik
            __self__.atoms.append(atom(x,y,z,ID,element,znacznik))
	## \brief Tworzy wierną kopję monomeru
    def replicate(__self__):
        new_atoms=[]
        new_bonds=[]
        for i in range (__self__.number_of_atoms):
            new_atoms.append(__self__.atoms[i])
        for i in range (__self__.number_of_bonds):
            new_bonds.append(__self__.bonds[i])
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms, __self__.number_of_bonds, new_bonds, __self__.wazne_atomy)
    ## \brief Obrót wszystkich atomu monomeru
    # \param m macierz obrotu
    def rotate_all(__self__,m):
        for i in range(__self__.number_of_atoms):
           x=__self__.atoms[i].x
           y=__self__.atoms[i].y
           z=__self__.atoms[i].z
           __self__.atoms[i].x=x*m[0][0]+y*m[0][1]+z*m[0][2]
           __self__.atoms[i].y=x*m[1][0]+y*m[1][1]+z*m[1][2]
           __self__.atoms[i].z=x*m[2][0]+y*m[2][1]+z*m[2][2]
	## \brief Przesunięcie wszystkich atomów monomeru
    # \param v wektor, o który następuje przesunięcie
    def translation_all(__self__, v):
        for i in range(__self__.number_of_atoms):
            __self__.atoms[i].x+=v.x
            __self__.atoms[i].y+=v.y
            __self__.atoms[i].z+=v.z
	## \brief Tworzy macierz układu współrzędnyc na C
	# \return Macierz układu
    def system_C(__self__):
        """ Tworzy macierz układu współrzędnych na karbonylowym atomie węgla. Tak aby oś x znajdowała się na wiązaniu C-OH, a oś y była prostopadła do grupy.
        """
        for i in range(len(__self__.atoms)):
            if __self__.atoms[i].znacznik=="Ckarb": C_karb=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="C_a": C_a=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="H": H=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="O_OH": O_OH=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="O=": O=__self__.atoms[i]
        x=O_OH.x-C_karb.x
        y=O_OH.y-C_karb.y
        z=O_OH.z-C_karb.z
        v_x=vector(x,y,z)
        a=v_x.leng()
        v_x.x=v_x.x/a
        v_x.y=v_x.y/a
        v_x.z=v_x.z/a
        x=O.x-C_karb.x
        y=O.y-C_karb.y
        z=O.z-C_karb.z
        v_CO=vector(x,y,z)
        v_y=v_x.vector_prod(v_CO)
        a=v_y.leng()
        v_y.x=v_y.x/a
        v_y.y=v_y.y/a
        v_y.z=v_y.z/a 
        v_z=v_x.vector_prod(v_y)
        a=v_z.leng()
        v_z.x=v_z.x/a
        v_z.y=v_z.y/a
        v_z.z=v_z.z/a
        A=[[v_x.x, v_y.x, v_z.x],[v_x.y, v_y.y, v_z.y], [v_x.z, v_y.z, v_z.z]]
        return(A)
	## \brief Tworzy macierz układu współrzędnyc na C
	# \return Macierz układu
    def system_N(__self__):
        """ Tworzy macierz układu współrzędnych na karbonylowym atomie węgla. Tak aby oś x znajdowała się na wiązaniu N-X, a oś y była prostopadła do atomów H i węgla alpha.
        """
        l=0
        for i in range(__self__.number_of_atoms):
            if __self__.atoms[i].znacznik=="C_a":
                C_a=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="N": N=__self__.atoms[i]
            if __self__.atoms[i].znacznik=="nH" and l==0:
                H1=__self__.atoms[i]
                __self__.atoms[i].znacznik="H1"
                l=1
            if __self__.atoms[i].znacznik=="nH" and l==1: 
                H2=__self__.atoms[i]
                __self__.atoms[i].znacznik="H2"
        x=-H1.x+N.x
        y=-H1.y+N.y
        z=-H1.z+N.z
        v_x=vector(x,y,z)
        a=v_x.leng()
        v_x.x=v_x.x/a
        v_x.y=v_x.y/a
        v_x.z=v_x.z/a
        x=H1.x-C_a.x
        y=H1.y-C_a.y
        z=H1.z-C_a.z
        v_CH1=vector(x,y,z)
        x=H2.x-C_a.x
        y=H2.y-C_a.y
        z=H2.z-C_a.z
        v_CH2=vector(x,y,z)
        v_y=v_CH1.vector_prod(v_CH2)
        a=v_y.leng()
        v_y.x=v_y.x/a
        v_y.y=v_y.y/a
        v_y.z=v_y.z/a
        v_z=v_x.vector_prod(v_y)
        a=v_z.leng()
        v_z.x=v_z.x/a
        v_z.y=v_z.y/a
        v_z.z=v_z.z/a         
        B=[[v_x.x, v_y.x, v_z.x],[v_x.y, v_y.y, v_z.y], [v_x.z, v_y.z, v_z.z]]
        return(B)
	## \brief Usuwa atom
	# \param ID ID atomu który będzie usunięty
    def remove(__self__, ID):
        for i in range(__self__.number_of_atoms):
            if __self__.atoms[i].ID==ID:
                __self__.atoms.pop(i)
                __self__.number_of_atoms-=1
                break
	## \brief Pozwala na wydrukowanie monomru
    def __str__(__self__):
        string="ID:  "+__self__.ID + "    Number of atoms:   " + str(__self__.number_of_atoms) + '\n'
        for i in range(__self__.number_of_atoms):       
            string+=  ( '%6s %2s %7.4f %7.4f %7.4f %6s' %(__self__.atoms[i].ID,__self__.atoms[i].element, __self__.atoms[i].x,__self__.atoms[i].y,__self__.atoms[i].z, __self__.atoms[i].znacznik))
            string+='\n'
        string+="Number of bonds:  " + str(__self__.number_of_bonds)+ '\n'
        for i in range(__self__.number_of_bonds):
            string+= ('%6s %6s %6s' %(__self__.bonds[i][0], __self__.bonds[i][1], __self__.bonds[i][2] ))+'\n'
        return string
## \brief Peptydy
# \author Bernadeta Nowosielska
# \param coord tablica zawierajaca tablicę, która zawiera ID monomeru, jego licznik oraz tablię obiektów klasy atom.
class peptide:
    coord=[]
    A=[]
	## \brief Dodaje pierwszy monomer do peptydu
	# \param monomer1 obiekt klasy monomer
    def start(__self__, monomer1):
        m1=monomer1.replicate()
        for i in range(m1.number_of_atoms):
            if m1.atoms[i].znacznik=="Ckarb": C=m1.atoms[i]
        v=vector(-C.x, -C.y, -C.z)
        m1.translation_all(v)
        __self__.A=m1.system_C()
        m1_table=[m1.ID, 1 , m1.atoms]
        __self__.coord.append(m1_table) 
	## \brief Dodaje kolejne monomery
	# \param monomer3 dodawany monomer
	# \param omega_i, fi_i, psi_i kąty torsyjne, które zostaną ustawione
    def add(__self__, monomer3, omega_i, fi_i, psi_i):
        m3=monomer3.replicate()
        lp=len(__self__.coord)
        for i in range(len(__self__.coord[lp-1][2])):
            if __self__.coord[lp-1][2][i].znacznik=="Ckarb": m1_C_karb=__self__.coord[lp-1][2][i]
            if __self__.coord[lp-1][2][i].znacznik=="C_a": m1_C_a=__self__.coord[lp-1][2][i]
            if __self__.coord[lp-1][2][i].znacznik=="O_OH": 
                m1_OH=__self__.coord[lp-1][2][i]
                licznik_OH=i
            if __self__.coord[lp-1][2][i].znacznik=="H": m1_H_ID=__self__.coord[lp-1][2][i].ID
        for i in range(m3.number_of_atoms):
            if m3.atoms[i].znacznik=="N": m3_N=m3.atoms[i]
            if m3.atoms[i].znacznik=="C_a": m3_C_a=m3.atoms[i]
            if m3.atoms[i].znacznik=="Ckarb": m3_C_karb=m3.atoms[i]
            if m3.atoms[i].znacznik=="O_OH": m3_O_OH=m3.atoms[i]
        x=-m3_N.x
        y=-m3_N.y
        z=-m3_N.z
        v2=vector(x,y,z)
        m3.translation_all(v2)
        B=m3.system_N()
        m3.rotate_all(transpose(B))
        m3.rotate_all(__self__.A)
        x=m1_OH.x
        y=m1_OH.y
        z=m1_OH.z
        v3=vector(x,y,z)
        a=v3.leng()
        v3.x=v3.x/a*1.4
        v3.y=v3.y/a*1.4
        v3.z=v3.z/a*1.4
        m3.translation_all(v3)
        b1=vector(m1_C_karb.x-m1_C_a.x, m1_C_karb.y-m1_C_a.y, m1_C_karb.z-m1_C_a.z)
        b2=vector(m3_N.x-m1_C_karb.x, m3_N.y-m1_C_karb.y, m3_N.z-m1_C_karb.z) 
        b3=vector(m3_C_a.x-m3_N.x, m3_C_a.y-m3_N.y, m3_C_a.z-m3_N.z)
        omega_temp = dihedral_angle(b1, b2, b3)
        omega=omega_temp - omega_i
        __self__.rotate_da("omega", omega , m3_N, m1_C_karb,m3) 
        b1=vector(m3_N.x-m1_C_karb.x, m3_N.y-m1_C_karb.y, m3_N.z-m1_C_karb.z) 
        b2=vector(m3_C_a.x-m3_N.x, m3_C_a.y-m3_N.y, m3_C_a.z-m3_N.z)
        b3=vector(m3_C_karb.x-m3_C_a.x, m3_C_karb.y-m3_C_a.y, m3_C_karb.z-m3_C_a.z)
        fi_temp = dihedral_angle(b1, b2, b3)
        fi=fi_temp - fi_i
        __self__.rotate_da("fi", fi ,m3_C_a, m3_N,m3)
        b1=vector(m3_C_a.x-m3_N.x, m3_C_a.y-m3_N.y, m3_C_a.z-m3_N.z)
        b2=vector(m3_C_karb.x-m3_C_a.x, m3_C_karb.y-m3_C_a.y, m3_C_karb.z-m3_C_a.z)
        b3=vector(m3_O_OH.x-m3_C_karb.x, m3_O_OH.y-m3_C_karb.y, m3_O_OH.z-m3_C_karb.z)
        psi_temp = dihedral_angle(b1, b2, b3)
        psi=psi_temp - psi_i
        __self__.rotate_da("psi", psi ,m3_C_karb, m3_C_a,m3)
        for i in range(m3.number_of_atoms):
            if m3.atoms[i].znacznik=="H1": m3_H1_ID=m3.atoms[i].ID
        __self__.A=m3.system_C()
        __self__.coord[lp-1][2].pop(licznik_OH)
        for i in range(len(__self__.coord[lp-1][2])):
            if __self__.coord[lp-1][2][i].znacznik=="H": licznik_H=i
        __self__.coord[lp-1][2].pop(licznik_H)
        m3.remove(m3_H1_ID)
        licznik_monomerow=1
        for i in range(lp):
            if __self__.coord[i][0]==m3.ID: licznik_monomerow+=1
        m3_table=[m3.ID, licznik_monomerow , m3.atoms]
        __self__.coord.append(m3_table)
        x=-m3_C_karb.x
        y=-m3_C_karb.y
        z=-m3_C_karb.z
        v4=vector(x,y,z)
	## \brief Pozwala na wydrukowanie peptydu
    def __str__(__self__):
        string=""
        for i in range(len(__self__.coord)):
            for j in range(len(__self__.coord[i][2])):
                string+=('%3s  %7.4f  %7.4f  %7.4f' %(__self__.coord[i][2][j].element,__self__.coord[i][2][j].x,__self__.coord[i][2][j].y,__self__.coord[i][2][j].z))
                string+='\n'
        return string
	## \brief Obraca o kąt torsyjny
	# \param type_ wybrany kąt torsyjn "omega", "fi" lub "psi"
	# \param angle wartość o którą nastąpi obrót
	# \param N, C końcowy i początkowy atom wiązania, na którym będzie następować obrót (obiekt klasy atom)
	# \param m3 monomer, który będzie obracany
    def rotate_da(__self__, type_, angle, N, C, m3):
        v1=vector(-N.x, -N.y, -N.z)
        len_peptide=len(__self__.coord)
        m3.translation_all(v1)
        for i in range(len_peptide):
            for j in range(len(__self__.coord[i][2])):
                __self__.coord[i][2][j].translation(v1)
        v2=vector((N.x-C.x),(N.y-C.y), (N.z-C.z))
        a=v2.leng()
        v2.x=v2.x/a
        v2.y=v2.y/a
        v2.z=v2.z/a
        M=[]
        M1=[math.cos(angle)+v2.x*v2.x*(1-math.cos(angle)), v2.x*v2.y*(1-math.cos(angle))+v2.z*math.sin(angle), v2.z*v2.x*(1-math.cos(angle))-v2.y*math.sin(angle)]
        M2=[v2.x*v2.y*(1-math.cos(angle))-v2.z*math.sin(angle),math.cos(angle)+v2.y*v2.y*(1-math.cos(angle)), v2.z*v2.y*(1-math.cos(angle))+v2.x*math.sin(angle) ]
        M3=[v2.x*v2.z*(1-math.cos(angle))+v2.y*math.sin(angle), v2.z*v2.y*(1-math.cos(angle))-v2.x*math.sin(angle), math.cos(angle)+v2.z*v2.z*(1-math.cos(angle))]
        M.append(M1)
        M.append(M2)
        M.append(M3)
        MM=[]
        MM1=[math.cos(-angle)+v2.x*v2.x*(1-math.cos(-angle)), v2.x*v2.y*(1-math.cos(-angle))+v2.z*math.sin(-angle), v2.z*v2.x*(1-math.cos(-angle))-v2.y*math.sin(-angle)]
        MM2=[v2.x*v2.y*(1-math.cos(-angle))-v2.z*math.sin(-angle),math.cos(-angle)+v2.y*v2.y*(1-math.cos(-angle)), v2.z*v2.y*(1-math.cos(-angle))+v2.x*math.sin(-angle) ]
        MM3=[v2.x*v2.z*(1-math.cos(-angle))+v2.y*math.sin(-angle), v2.z*v2.y*(1-math.cos(-angle))-v2.x*math.sin(-angle), math.cos(-angle)+v2.z*v2.z*(1-math.cos(-angle))]
        MM.append(MM1)
        MM.append(MM2)
        MM.append(MM3)
        if type_=="fi" or type_=="omega":
            m3.rotate_all(M)
        if type_=="fi":
            for i in range(m3.number_of_atoms):
                if m3.atoms[i].znacznik=="H2":
                    m3.atoms[i].rotate(MM)
        if type_=="psi":
            for i in range(m3.number_of_atoms):
                if m3.atoms[i].znacznik=="O=" or m3.atoms[i].znacznik=="O_OH" or m3.atoms[i].znacznik=="H":
                    m3.atoms[i].rotate(M)
## \brief Transpozyjcja macierzy
# \param m maciwerz, która ma zostać zmieniona
# \return macierz transponowana
# \author Bernadeta Nowosielska
def transpose(m):
    temp=[]
    c1=[m[0][0],m[1][0],m[2][0]]
    c2=[m[0][1],m[1][1],m[2][1]]
    c3=[m[0][2],m[1][2],m[2][2]]
    temp=[c1,c2,c3]
    return temp 
## \brief Wyznaczanie kąta torsyjnego
# \param b1, b2, b3 trzy wektory pomiędzy, którymi liczony jest kąt torsyjny
# \return wartość kąta torsyjnego
# \author Bernadeta Nowosielska
def dihedral_angle(b1, b2, b3):
    x=((b1.vector_prod(b2)).vector_prod(b2.vector_prod(b3))).scalar_prod(b2)/b2.leng()
    y=(b1.vector_prod(b2)).scalar_prod(b2.vector_prod(b3))
    return math.atan2(x,y)
def upload_data(table, l1, l2, l3, l4, l5, l7, l8):
    atoms_param=[]  #parametry kolejnych atomow
    no_at=0  #number of atoms
    ID="?"
    no_bonds=0
    bonds=[]
    znacznik=""
    wazne_atomy=[]
    wodor="brak"
    tlen="brak"
    wegiel="brak"
    tlen_doub="brak"
    azot="brak"
    amino_hydrogen=[]
    for w1 in range (0,len(table)):
        if table[w1][0]==table[1][1]:
            if len(table[w1])>=12 and (table[w1][12]!="?" or table[w1][13]!="?" or table [w1][14]!="?" ) and (table[w1][12]!="charge") :
                ID=table[w1][0]     # ID of monomer
                atom_name=table[w1][1]    #ID of atom (specific only within one monomer)
                element=table[w1][3]  # name of the element 
                x=float(table[w1][12])
                y=float(table[w1][13])
                z=float(table[w1][14])
                if table[w1][1]=='C': 
                    znacznik="Ckarb"
                else: znacznik=""
                atom_i = atom(x,y,z,atom_name,element,znacznik) #obiekt klasy atom
                no_at+=1
                atoms_param.append(atom_i) #tablica zawierająca obiekty klasy atom
            if len(table[w1])==7 and table[w1][6]==str(no_bonds+1):
                bonds.append([table[w1][1], table[w1][2], table[w1][3] ])
                no_bonds+=1
               
    for w2 in range (0, len(bonds)):
       if ((bonds[w2][0]=="C" and ("O" in bonds[w2][1])) or (bonds[w2][1]=="C" and  ("O" in bonds[w2][0]))) and bonds[w2][2]=="SING":
#           print (bonds[w2], ID)  # wiązanie C-Oh
           if ("O" in bonds[w2][0]): tlen=bonds[w2][0]
           else: tlen=bonds[w2][1] 
           if ("C" in bonds[w2][0]): wegiel=bonds[w2][0]
           else: wegiel=bonds[w2][1]
           for w3 in range (0, len(bonds)):
               if (("H" in bonds[w3][0]) or "H" in bonds[w3][1]) and (bonds[w3][0]==tlen or bonds[w3][1]==tlen) and (("O" in bonds[w3][0]) or ("O" in bonds[w3][1])):
                   #print (bonds[w3], ID)
                   if ("H" in bonds[w3][0]): wodor=bonds[w3][0]
                   else: wodor=bonds[w3][1]
               if (bonds[w3][2]=="DOUB" and (bonds[w3][0]==wegiel or bonds[w3][1]==wegiel)):
                   if ("O" in bonds[w3][0]): tlen_doub=bonds[w3][0]
                   else: tlen_doub=bonds[w3][1]
       if (bonds[w2][0]=="CA" and ("N" in bonds[w2][1])) or (bonds[w2][1]=="CA" and ("N" in bonds[w2][0])): 
           if "N" in bonds[w2][1]: azot=bonds[w2][1] 
           else: azot=bonds[w2][0]
           for w5 in range (0, len(bonds)):
               if (bonds[w5][0]==azot and ("H" in bonds[w5][1])) or (bonds[w5][1]==azot and ("H" in bonds[w5][0])):
                   if "H" in bonds[w5][0]: amino_hydrogen.append(bonds[w5][0])
                   else: amino_hydrogen.append(bonds[w5][1])       
                           
    for w4 in range (0, len(atoms_param)):
       if atoms_param[w4].ID==wodor:
          atoms_param[w4].znacznik="H"
          wazne_atomy.append(atoms_param[w4])
#          print (ID, atoms_param[w4])           
          l1.append(1)
       if atoms_param[w4].ID==tlen:                         
          atoms_param[w4].znacznik="O_OH"
          wazne_atomy.append(atoms_param[w4])
#          print (ID, atoms_param[w4])          
          l2.append(1)
       if atoms_param[w4].ID==wegiel:
          wazne_atomy.append(atoms_param[w4]) 
#          print (ID, atoms_param[w4])
          l3.append(1)
       if atoms_param[w4].ID==tlen_doub:
          atoms_param[w4].znacznik="O="                           
          wazne_atomy.append(atoms_param[w4])
#          print (ID, atoms_param[w4])
          l4.append(1)
       if atoms_param[w4].ID=="CA":
          atoms_param[w4].znacznik="C_a"
          wazne_atomy.append(atoms_param[w4])
#          print (ID, atoms_param[w4])
          l5.append(1)
    if len(wazne_atomy)!=5: ID="?"
    for w4 in range (0, len(atoms_param)):
       if atoms_param[w4].ID==azot:
          atoms_param[w4].znacznik="N"
          wazne_atomy.append(atoms_param[w4])
#          print (ID, atoms_param[w4])
          l7.append(1)
       for w6 in range(0,len(amino_hydrogen)):
           if atoms_param[w4].ID==amino_hydrogen[w6]:
               atoms_param[w4].znacznik="nH"
               wazne_atomy.append(atoms_param[w4])
#               print (ID, atoms_param[w4])
               l8.append(1)
#    print(len(wazne_atomy))
#    print (len(l1), len(l2), len(l3), len(l4), len(l5), len(l7), len(l8))
    if len(wazne_atomy)!=8: ID="?"
    return  monomer(ID, no_at, atoms_param, no_bonds , bonds, wazne_atomy)

def make_output(peptyd, i, j, n):
    string=""
    string+=('%5s %5d %-7s %-7s %8.3f %8.3f %8.3f %3s' %("ATOM ", n, peptyd.coord[i][2][j-1].ID, peptyd.coord[i][0], peptyd.coord[i][2][j-1].x, peptyd.coord[i][2][j-1].y, peptyd.coord[i][2][j-1].z, peptyd.coord[i][2][j-1].element))
    string+='\n'
    f.write(string)

file=open('Components-pub.cif')
i=0
table =[]
number_of_lines=0
monomers_list={}
l1=[]
l2=[]
l3=[]
l4=[]
l5=[]
l6=0
l7=[]
l8=[]
for line in file:  
    i+=1
    if i>21362: break
#    if i>8355: break
#    if i>3785: break
    words=re.split("\s+",line.strip())
    table.append(words)
    number_of_lines+=1
    if words[0][0:5]!="data_": continue
    if i==3: 
       table = [] 
       continue
    for j in range(0,10):
        if table[j][0]=="_chem_comp.type":
            if table[j][1][1:10]=="L-peptide" or table[j][1][1:10]=="L-PEPTIDE" or ("GLY" in table[j-2]):
    # making monomer
               monomer_i=upload_data(table, l1, l2, l3, l4, l5, l7, l8)
               if monomer_i.ID!="?":
                   monomers_list[monomer_i.ID]=monomer_i
                   l6+=1
#                   print (l6)
                   
    table =[]
    number_of_lines=0
#for key in monomers_list:
#    print(key)
#    monomers_list[key].system_N()
#print(len(monomers_list))

data=open(sys.argv[1])
words2=""
table2=[]
for line in data:
    words2=re.split("\s+",line.strip())
    table2.append(words2)


aa=peptide()
aa.start(monomers_list[table2[0][0]])
for w9 in range (0, (len(table2)-1)):
#    print (w9)
    aa.add(monomers_list[table2[w9+1][0]],math.pi,  float(table2[w9+1][1]), float(table2[w9+1][2]))
#print(aa)

f=open('output.pdb', 'w')
i=0
j=0
n=0
for w7 in range (len(aa.coord)):
    for w8 in range (len(aa.coord[w7][2])):
        n+=1
        make_output(aa, w7, w8, n)