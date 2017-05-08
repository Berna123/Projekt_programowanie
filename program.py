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
    def __init__(__self__,a,b,c,ID,element):
        __self__.x=a
        __self__.y=b
        __self__.z=c
        __self__.ID=ID
        __self__.element=element
    def scalar_prod(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    def rotate_prod(__self__,m):
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
        return ( '%6s %2s %7.4f %7.4f %7.4f' %(__self__.ID,__self__.element, __self__.x,__self__.y,__self__.z, ))
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
            __self__.atoms.append(atom(x,y,z,ID,element))
    def replicate(__self__):
        new_atoms=[]
        for i in range (__self__.number_of_atoms):
            new_atoms.append(__self__.atoms[i])
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms)
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
            string+=  ( '%6s %2s %7.4f %7.4f %7.4f' %(__self__.atoms[i].ID,__self__.atoms[i].element, __self__.atoms[i].x,__self__.atoms[i].y,__self__.atoms[i].z, ))
            string+='\n'
        string+="Number of bonds:  " + str(__self__.number_of_bonds)+ '\n'
        for i in range(__self__.number_of_bonds):
            string+= ('%6s %6s %6s' %(__self__.bonds[i][0], __self__.bonds[i][1], __self__.bonds[i][2] ))+'\n'
        return string       
### tworzy obiekt klasy atom, następnie z atomow obiekt monomer klasy monomer, replikuje monomer do nowego obiektu
def upload_data(table):
    atoms_param=[]  #parametry kolejnych atomow
    no_at=0  #number of atoms
    ID="?"
    no_bonds=0
    bonds=[]
    for w1 in range (0,len(table)):
        if table[w1][0]==table[1][1]:
            if len(table[w1])>=12 and (table[w1][12]!="?" or table[w1][13]!="?" or table [w1][14]!="?" ) and (table[w1][12]!="charge") :
                ID=table[w1][0]     # ID of monomer
                atom_name=table[w1][2]    #ID of atom (specific only within one monomer)
                element=table[w1][3]  # name of the element 
                x=float(table[w1][12])
                y=float(table[w1][13])
                z=float(table[w1][14])
                atom_i = atom(x,y,z,atom_name,element) #obiekt klasy atom
                no_at+=1
                atoms_param.append(atom_i) #tablica zawierająca obiekty klasy atom
            if len(table[w1])==7 and table[w1][6]==str(no_bonds+1):
                bonds.append([table[w1][1], table[w1][2], table[w1][3] ])
                no_bonds+=1
#    print(monomer(ID, no_at, atoms_param))
    return  monomer(ID, no_at, atoms_param, no_bonds , bonds) 
file=open('Components-pub.cif')
i=0
table =[]
number_of_lines=0
monomers_list=[] 
for line in file:  
    i+=1
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
               monomer_i=upload_data(table)
               if monomer_i.ID!="?":
                   monomers_list.append(monomer_i)
    table =[]
    number_of_lines=0
for l in range (len(monomers_list)):
    print (monomers_list[l])



        
    
    