# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 16:43:25 2017

@author: barbara
"""

import re
class vektor:
    x=0
    y=0
    z=0
    def __init__(__self__,a,b,c):
        __self__.x=a
        __self__.y=b
        __self__.z=c
class atom:
    x=0
    y=0
    z=0
    ID=""
    def __init__(__self__,a,b,c,ID):
        __self__.x=a
        __self__.y=b
        __self__.z=c
        __self__.ID=ID
    def scalar_prod(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    def matrix_prod(__self__,m):
        __self__.x=__self__.x*m[0][0]+__self__.y*m[1][0]+__self__.z*m[2][0]
        __self__.y=__self__.x*m[0][1]+__self__.y*m[1][1]+__self__.z*m[2][1]
        __self__.z=__self__.x*m[0][2]+__self__.y*m[1][2]+__self__.z*m[2][2]
    def translation(__self__,v):
        __self__.x+=v.a
        __self__.y+=v.b
        __self__.z+=v.z
    def vector_prod(__self__,p):
        w=vektor(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    def __str__(__self__):
        return ( __self__.ID.ljust(4) + str(__self__.x).rjust(8) + str(__self__.y).rjust(8) + str(__self__.z).rjust(8))   
class monomer:
    ID=""
    atoms= []
    number_of_atoms = 0
    def __init__(__self__,ID,noa, atoms):
        __self__.ID=ID
        __self__.number_of_atoms=noa
        for i in range (noa):
            (__self__.atoms).append(atoms[i])
    def replicate(__self__):
        new_atoms=[]
        for i in range (__self__.number_of_atoms):
            new_atoms.append(__self__.atoms[i])
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms)
    def __str__(__self__):
        string="ID:  "+__self__.ID + "    Number of atoms:   " + str(__self__.number_of_atoms) + '\n'
        for i in range(__self__.number_of_atoms):
            string+= (__self__.atoms[i].ID.ljust(4) + str(__self__.atoms[i].x).rjust(8) + str(__self__.atoms[i].y).rjust(8) + str(__self__.atoms[i].z).rjust(8) + '\n')
        return string
        
### tworzy obiekt klasy atom, następnie z atomow obiekt monomer klasy monomer, replikuje monomer do nowego obiektu
def upload_data(table):
    atoms_param=[]  #parametry kolejnych atomow
    no_at=0  #number of atoms
    for w1 in range (0,len(table)):
        if table[w1][0]==table[1][1]:
            if len(table[w1])>=12:
                ID=table[w1][0]     # ID of monomer
                atom_name=table[w1][2]    #ID of atom (specific only within one monomer)
                pierwiastek=table[w1][3]  # name of the element 
                x=float(table[w1][12])
                y=float(table[w1][13])
                z=float(table[w1][14])
                atom_i = atom(x,y,z,atom_name) #obiekt klasy atom
                no_at+=1
                atoms_param.append(atom_i) #tablica zawierająca parametry atomow danego monomeru
    monomer_i = monomer(ID, no_at, atoms_param) 
    monomer_i.replicate()
    print (monomer_i)

        
#def export_data(table):
file=open('Components-pub.cif')
i=0
table =[]
number_of_lines=0
for line in file:
    
    i+=1
    if i>8355: break
    words=re.split("\s+",line.strip())
    table.append(words)
    number_of_lines+=1
    if words[0][0:5]!="data_": continue
    if i==3: 
       for j in range(number_of_lines):
           table.pop()
       number_of_lines=0 
       continue
    if table[3][1][1:10]=="L-peptide" or table[3][1][1:10]=="L-PEPTIDE":
        print(i)
        
# making monomer
        upload_data(table)

#        export_data(table)
    for j in range(number_of_lines):
        table.pop()
    number_of_lines=0
        
    
    