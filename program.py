import re
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
### klasa do napisania ###
#class monomer:
### funkcja do napisania ###        
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
#        export_data(table)
    for j in range(number_of_lines):
        table.pop()
    number_of_lines=0
        
    
    