import re
import math
class vector:
    x=0
    y=0
    z=0
    def __init__(__self__,a,b,c):
        __self__.x=a
        __self__.y=b
        __self__.z=c
    def leng (__self__):
        return math.sqrt(__self__.x*__self__.x + __self__.y*__self__.y + __self__.z*__self__.z )
    def vector_prod(__self__,p):
        w=vector(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    def scalar_prod(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    def __str__(__self__):
        return "[ "+str(__self__.x) + ", "+str(__self__.y) + ", "+str(__self__.y) + "]"
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
        w=vector(0,0,0)
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
    def __init__(__self__,ID,noa, atoms, nob, bonds, wazne_atomy):
        __self__.atoms= []
        __self__.bonds= []
        __self__.wazne_atomy=[]
        for i in range(len(wazne_atomy)):
            __self__.wazne_atomy.append(wazne_atomy[i])
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
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms, __self__.number_of_bonds, new_bonds, __self__.wazne_atomy)
    def rotate_all(__self__,m):
        for i in range(__self__.number_of_atoms):
           x=__self__.atoms[i].x
           y=__self__.atoms[i].y
           z=__self__.atoms[i].z
           __self__.atoms[i].x=x*m[0][0]+y*m[0][1]+z*m[0][2]
           __self__.atoms[i].y=x*m[1][0]+y*m[1][1]+z*m[1][2]
           __self__.atoms[i].z=x*m[2][0]+y*m[2][1]+z*m[2][2]
    def translation_all(__self__, v):
        for i in range(__self__.number_of_atoms):
            __self__.atoms[i].x+=v.x
            __self__.atoms[i].y+=v.y
            __self__.atoms[i].z+=v.z
    def system_C(__self__):
        for i in range(5):
            if __self__.wazne_atomy[i].znacznik=="Ckarb": C_karb=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="C_a": C_a=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="H": H=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="O_OH": O_OH=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="O=": O=__self__.wazne_atomy[i]
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
#        print(A)
    def system_N(__self__):
        l=0
        for i in range(8):
            if __self__.wazne_atomy[i].znacznik=="C_a":
                C_a=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="N": N=__self__.wazne_atomy[i]
            if __self__.wazne_atomy[i].znacznik=="nH" and l==0:
                H1=__self__.wazne_atomy[i]
                __self__.wazne_atomy[i].znacznik="H1"
                l=1
                H1_ID=__self__.wazne_atomy[i].ID
            if __self__.wazne_atomy[i].znacznik=="nH" and l==1: 
                H2=__self__.wazne_atomy[i]
                __self__.wazne_atomy[i].znacznik="H2"
        for i in range(__self__.number_of_atoms):
            if __self__.atoms[i].ID==H1_ID : __self__.atoms[i].znacznik="H1"
        x=H1.x-N.x
        y=H1.y-N.y
        z=H1.z-N.z
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
    def remove(__self__, ID):
        for i in range(__self__.number_of_atoms):
            if __self__.atoms[i].ID==ID:
                __self__.atoms.pop(i)
                __self__.number_of_atoms-=1
                break
    def __str__(__self__):
        string="ID:  "+__self__.ID + "    Number of atoms:   " + str(__self__.number_of_atoms) + '\n'
        for i in range(__self__.number_of_atoms):       
            string+=  ( '%6s %2s %7.4f %7.4f %7.4f %6s' %(__self__.atoms[i].ID,__self__.atoms[i].element, __self__.atoms[i].x,__self__.atoms[i].y,__self__.atoms[i].z, __self__.atoms[i].znacznik))
            string+='\n'
        string+="Number of bonds:  " + str(__self__.number_of_bonds)+ '\n'
        for i in range(__self__.number_of_bonds):
            string+= ('%6s %6s %6s' %(__self__.bonds[i][0], __self__.bonds[i][1], __self__.bonds[i][2] ))+'\n'
        return string
class peptide:
    coord=[]
    def synthesize(__self__,monomer1, monomer2):
        m1=monomer1.replicate()
        m2=monomer2.replicate()
        A=m1.system_C()
        B=m2.system_N()
        m2.rotate_all(transpose(B))
        m2.rotate_all(A)
        for i in range(m1.number_of_atoms):
            if m1.atoms[i].znacznik=="Ckarb": m1_C_karb=m1.atoms[i]
            if m1.atoms[i].znacznik=="O_OH": 
                m1_OH=m1.atoms[i]
                m1_OH_ID=m1.atoms[i].ID
            if m1.atoms[i].znacznik=="H": m1_H_ID=m1.atoms[i].ID
        for i in range(m2.number_of_atoms):
            if m2.atoms[i].znacznik=="N": m2_N=m2.atoms[i]
            if m2.atoms[i].znacznik=="C_a": m2_C_a=m2.atoms[i]
            if m2.atoms[i].znacznik=="H1": m2_H1_ID=m2.atoms[i].ID
        x=-m1_C_karb.x
        y=-m1_C_karb.y
        z=-m1_C_karb.z
        v1=vector(x,y,z)
        m1.translation_all(v1)
        x=-m2_N.x
        y=-m2_N.y
        z=-m2_N.z
        v2=vector(x,y,z)
        m2.translation_all(v2)
        m2
        A=m2.system_C()
        m1.remove(m1_H_ID)
        m1.remove(m1_OH_ID)
        m2.remove(m2_H1_ID)
        m1_table=[m1.ID, 1 , m1.atoms]
        __self__.coord.append(m1_table)
        m2_table=[m2.ID, 1 , m2.atoms]
        __self__.coord.append(m2_table)
    def __str__(__self__):
        string=""
        for i in range(len(__self__.coord)):
            for j in range(len(__self__.coord[i][2])):
                string+=('%3s  %7.4f  %7.4f  %7.4f' %(__self__.coord[i][2][j].element,__self__.coord[i][2][j].x,__self__.coord[i][2][j].y,__self__.coord[i][2][j].z))
                string+='\n'
        return string
### tworzy obiekt klasy atom, następnie z atomow obiekt monomer klasy monomer, replikuje monomer do nowego obiektu
def transpose(m):
    temp=[]
    c1=[m[0][0],m[1][0],m[2][0]]
    c2=[m[0][1],m[1][1],m[2][1]]
    c3=[m[0][2],m[1][2],m[2][2]]
    temp=[c1,c2,c3]
    return temp 
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
    for j in range(10):
        if table[j][0]=="_chem_comp.type":
            if table[j][1][1:10]=="L-peptide" or table[j][1][1:10]=="L-PEPTIDE":
    # making monomer
               monomer_i=upload_data(table, l1, l2, l3, l4, l5, l7, l8)
               if monomer_i.ID!="?":
                   monomers_list[monomer_i.ID]=monomer_i
                   l6+=1
#                   print (l6)
                   
    table =[]
    number_of_lines=0
#for key in monomers_list:
#    monomers_list[key].system_C()
#    monomers_list[key].system_N()
#print(len(monomers_list))
aa=peptide()
aa.synthesize(monomers_list["C3Y"], monomers_list["C3Y"])
print(aa)