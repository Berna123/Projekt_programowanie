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
        __self__.x=__self__.x*m[0][0]+__self__.y*m[1][0]+__self__.z*m[2][0]
        __self__.y=__self__.x*m[0][1]+__self__.y*m[1][1]+__self__.z*m[2][1]
        __self__.z=__self__.x*m[0][2]+__self__.y*m[1][2]+__self__.z*m[2][2]
    def translation(__self__,v):
        __self__.x+=v.x
        __self__.y+=v.y
        __self__.z+=v.z
    def vector_prod(__self__,p):
        w=vektor(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    def __str__(__self__):
        return ( '%6s %2s %7.4f %7.4f %7.4f %6s' %(__self__.ID,__self__.element, __self__.x,__self__.y,__self__.z, __self__.znacznik))
class monomer:
    ID=""
    number_of_atoms = 0
    number_of_bonds = 0
#    atoms=[]
    def __init__(__self__,ID,noa, atoms, nob, bonds):
        __self__.atoms= []
        __self__.bonds= []
        for i in range (nob):
            __self__.bonds.append(bonds[i])
#        print(len(__self__.atoms))
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
    def replicate(__self__):
        new_atoms=[]
        new_bonds=[]
        for i in range (__self__.number_of_atoms):
            new_atoms.append(__self__.atoms[i])
        for i in range (__self__.number_of_bonds):
            new_bonds.append(__self__.bonds[i])
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms, __self__.number_of_bonds, new_bonds)
    def rotate_all(__self__,m):
        for i in range(__self__.number_of_atoms):
           __self__.atoms[i].x=__self__.atoms[i].x*m[0][0]+__self__.atoms[i].y*m[1][0]+__self__.atoms[i].z*m[2][0]
           __self__.atoms[i].y=__self__.atoms[i].x*m[0][1]+__self__.atoms[i].y*m[1][1]+__self__.atoms[i].z*m[2][1]
           __self__.atoms[i].z=__self__.atoms[i].x*m[0][2]+__self__.atoms[i].y*m[1][2]+__self__.atoms[i].z*m[2][2]
    def translation_all(__self__, v):
        for i in range(__self__.number_of_atoms):
            __self__.atoms[i].x+=v.x
            __self__.atoms[i].y+=v.y
            __self__.atoms[i].z+=v.z
    def __str__(__self__):
        string="ID:  "+__self__.ID + "    Number of atoms:   " + str(__self__.number_of_atoms) + '\n'
        for i in range(__self__.number_of_atoms):       
            string+=  ( '%6s %2s %7.4f %7.4f %7.4f %6s' %(__self__.atoms[i].ID,__self__.atoms[i].element, __self__.atoms[i].x,__self__.atoms[i].y,__self__.atoms[i].z, __self__.atoms[i].znacznik))
            string+='\n'
        string+="Number of bonds:  " + str(__self__.number_of_bonds)+ '\n'
        for i in range(__self__.number_of_bonds):
            string+= ('%6s %6s %6s' %(__self__.bonds[i][0], __self__.bonds[i][1], __self__.bonds[i][2] ))+'\n'
        return string       
### tworzy obiekt klasy atom, następnie z atomow obiekt monomer klasy monomer, replikuje monomer do nowego obiektu
def upload_data(table, basia, basia2):
    atoms_param=[]  #parametry kolejnych atomow
    no_at=0  #number of atoms
    ID="?"
    no_bonds=0
    bonds=[]
    znacznik=""
    wazne_atomy=[]
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
                    #print (table[w1])
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
           
           basia.append(ID)
           for w3 in range (0, len(bonds)):
               if (("H" in bonds[w3][0]) or "H" in bonds[w3][1]) and (bonds[w3][0]==tlen or bonds[w3][1]==tlen) and (("O" in bonds[w3][0]) or ("O" in bonds[w3][1])):
                   #print (bonds[w3], ID)
                   if ("H" in bonds[w3][0]): wodor=bonds[w3][0]
                   else: wodor=bonds[w3][1]
                   
                   basia2.append(ID)
                   for w4 in range (0, len(atoms_param)):
                       if atoms_param[w4].ID==wodor:
#                           print (ID, atoms_param[w4])                         
                           wazne_atomy.append(atoms_param[w4])
                       if atoms_param[w4].ID==tlen:                         
#                           print (ID, atoms_param[w4])
                           wazne_atomy.append(atoms_param[w4])
                       if atoms_param[w4].ID==wegiel:
#                           print (ID, atoms_param[w4])
                           wazne_atomy.append(ID)
                           wazne_atomy.append(atoms_param[w4])       
    for w5 in range (0, len(wazne_atomy)):
        print (wazne_atomy[w5])                       

#           print (len(basia), len(basia2)) #basia - ilosc znalezionych wiązan raczej wegla karboksylowego z raczej tlenem 
                                         #basia2 - ilosc O-H przylaczonych do znalezionego wczesniej wegla

#    print(monomer(ID, no_at, atoms_param))
    return  monomer(ID, no_at, atoms_param, no_bonds , bonds)
file=open('Components-pub.cif')
i=0
table =[]
number_of_lines=0
monomers_list={}
spr=0
basia=[]
basia2=[]
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
    for j in range(10):
        if table[j][0]=="_chem_comp.type":
            if table[j][1][1:10]=="L-peptide" or table[j][1][1:10]=="L-PEPTIDE":
    # making monomer
               monomer_i=upload_data(table, basia, basia2)
               if monomer_i.ID!="?":
                   monomers_list[monomer_i.ID]=monomer_i
                   spr+=1
                   
    table =[]
    number_of_lines=0
#for l in range (len(monomers_list)):
#    print (monomers_list[l])

#for key in monomers_list:
#    print(monomers_list[key])
    
    
print (spr)
