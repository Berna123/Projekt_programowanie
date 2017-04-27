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
class monomer:
    ID=""
    atoms= []
    number_of_atoms = 0
    def __init__(__self__,ID,noa, atoms):
        __self__.ID=ID
        __self__.number_of_atoms=noa
        for i in range (noa):
            atoms.append(atoms(i))
    def replicate(__self__):
        new_atoms=[]
        for i in range (__self__.number_of_atoms):
            new_atoms.append(__self__.atoms(i))
        return monomer(__self__.ID,__self__.number_of_atoms, new_atoms)
### funkcja do napisania ###        
#def export_data(table):
file=open('Components-pub.cif')
i=0
table =[]
number_of_lines=0
for line in file:
    
    atoms_param=[]  #parametry kolejnych atomow
    no_at=0
    
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
#basia - ma tworzyć obiekt klasy atom i z atomu obiekt klasy monomer; 

        for w1 in range (40,len(table)):
            if table[w1][0]==table[1][1]:
                if len(table[w1])>=12:
                    ID=table[w1][0]  
                    atom_name=table[w1][2] 
                    pierwiastek=table[w1][3] 
                    x=table[w1][12]
                    y=table[w1][13]
                    z=table[w1][14]
                    atom_i = atom(x,y,z,atom_name) #to powinien być obiekt klasy atom, ale nie wygląda jak powinien
                    no_at+=1
                    atoms_param.append(atom_i)
        monomer_i = monomer(ID, no_at, atoms_param) #nie może go stworzyć, bo pa problem z atoms_param(bo chyba jest źle stworzony)
        monomer_i.replicate()
        print (ID, no_at, atoms_param)
        
#        export_data(table)
    for j in range(number_of_lines):
        table.pop()
    number_of_lines=0
        
    
    