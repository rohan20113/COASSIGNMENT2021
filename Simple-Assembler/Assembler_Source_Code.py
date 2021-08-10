def typeA(a,b,c,d):
    reg["FLAGS"]="0"*16 #setting of overflow flag can be wrong please have a look
    x=int(reg[c][1],2)
    y=int(reg[d][1],2)
    if(a=="add"):
        z=x+y
        if z>65535:
            reg["FLAGS"][1][12:13]="1"
    elif(a=="sub"):
        z=x-y
        if x-y<0:
            reg["FLAGS"][1][12:13]="1"
            z=0
    elif(a=="and"):
        z=x&y
    elif(a=="mul"):
        z=x*y
        if z>65535:
            reg["FLAGS"][1][12:13]="1"
    elif(a=="or"):
        z=x|y
    elif(a=="xor"):
        z=x^y    
    f=bin(z)
    f=f[2:]
    if len(f)>16:
        f=f[len(f)-16:]
    f.rjust(16,"0")
    reg[b][1]=f

    return (opcode[a]+"00"+reg[b][0]+reg[c][0]+reg[d][0])
