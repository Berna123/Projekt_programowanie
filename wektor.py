class wektor:
    x=0
    y=0
    z=0
    def __init__(__self__,a,b,c):
        __self__.x=a
        __self__.y=b
        __self__.z=c
    def skalarny(__self__,p):
        s=__self__.x*p.x+__self__.y*p.y+__self__.z*p.z
        return s
    def wektorowy(__self__,p):
        w=wektor(0,0,0)
        w.x=__self__.y*p.z-__self__.z*p.y
        w.y=-__self__.x*p.z+__self__.z*p.x
        w.z=__self__.x*p.y-__self__.y*p.x
        return w
    def __str__(__self__):
        return("["+str(__self__.x)+","+str(__self__.y)+","+str(__self__.z)+"]")
w1=wektor(1,0,0)
print(w1)
w1=wektor(0,1,0)
#print(w1.skalarny(w2))
print(w1)