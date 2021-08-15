
reg={ "R0":["000","0"*16],"R1":["001","0"*16],"R2":["010","0"*16],"R3":["011","0"*16],"R4":["100","0"*16],"R5":["101","0"*16],"R6":["110","0"*16],"FLAGS":["111","0000000000001111"]}

def typeA(u):
    reg["FLAGS"][1]="0"*16 #setting of overflow flag can be wrong please have a look
    # x=int(reg[u[2]][1],2)
    # y=int(reg[u[3]][1],2)
    opcode=""
    if(u[0]=="add"):
        opcode+="0000000"
        # z=x+y
        # if z>65535:
        #     reg["FLAGS"][1]="0000000000001000"
    elif(u[0]=="sub"):
        opcode+="0000100"
        # z=x-y
        # if z<0:
        #     reg["FLAGS"][1]="0000000000001000"
        #     z=0
    elif(u[0]=="and"):
        opcode+="0110000"
        # z=x&y
    elif(u[0]=="mul"):
        opcode+="0011000"
        # z=x*y
        # if z>65535:
        #     reg["FLAGS"][1]="0000000000001000"
    elif(u[0]=="or"):
        opcode+="0101100"
        # z=x|y
    elif(u[0]=="xor"):
        opcode+="0101000"
        # z=x^y
    else:
        # print("Wrong Syntax")
        return

    opcode+=reg[u[1]][0]+reg[u[2]][0]+reg[u[3]][0]

    # f=bin(z)
    # f=f[2:]
    # if len(f)>16:   
    #     f=f[-16:]
    # f=f.rjust(16,"0")
    # reg[u[1]][1]=f

    return(opcode)

def typeB(u):
    temp_int=int(u[2][1:])
    temp=bin(temp_int)[2:]
    imm=temp.rjust(8, "0")
    temp=temp.rjust(16, "0")
    op=""
    if(u[0]=="mov"):
        op+="00010"
        reg[u[1]][1]=temp_int
    elif(u[0]=="rs"):
        op+="01000"
        acc="0"*temp_int
        temp=acc+temp
        temp=temp[:16]
        reg[u[1]][1]=temp
    elif(u[0]=="ls"):
        op+="01001"
        acc="0"*temp_int
        temp=temp+acc
        temp=temp[-16:]
        reg[u[1]][1]=temp
    else:
        print("Wrong Syntax")
        return
    op+=reg[u[1]][0]   
    op+=imm
    return(op)

def typeC(u):
    reg["FLAGS"][1]="0000000000000000"
    op=""
    if(u[0]=="mov"):
        op+="0001100000"
        reg[u[1]][1]=reg[u[2]][1]
        # op+=reg[u[1]][0]+reg[u[2]][0]
    elif(u[0]=="div"):
        op+="0011100000"
        # a= int(reg[u[1]], 2)
        # b= int(reg[u[2]], 2)
        # quo=int(a/b)
        # rem=a%b
        # bin_quo=bin(quo)[2:]
        # bin_rem=bin(rem)[2:]
        # bin_quo=bin_quo.rjust(16, "0")
        # bin_rem=bin_rem.rjust(16, "0")
        # reg["R0"][1]=bin_quo
        # reg["R1"][1]=bin_rem
    elif(u[0]=="not"):
        op+="0110100000"
        # temp=reg[u[2]][1]
        # inv_temp=""
        # for i in temp:
        #     if(i=="1"):
        #         inv_temp+="0"
        #     else:
        #         inv_temp+="1"
    elif(u[0]=="cmp"):
        op+="0111000000"
        # a= int(reg[u[1]][1], 2)
        # b= int(reg[u[2]][1], 2)
        # if(a<b):
        #     reg["FLAGS"][1]="0000000000000100"
        # elif(a>b):
        #     reg["FLAGS"][1]="0000000000000010"
        # elif(a==b):
        #     reg["FLAGS"][1]="0000000000000001"
    # else:
        # print("Wrong Syntax")
        # return
    op+=reg[u[1]][0]+reg[u[2]][0]
    return(op)

# def typeD(u): #u[2]
#     op=""
#     if(u[0]=="ld"):
#         op+="00100"+reg[u[1]][0]
#         temp=var_add[u[2]][0]
#         reg[u[1]][1]=temp
#     elif(u[0]=="st"):
#         op+="00101"+reg[u[1]][0]
#         var_add[u[2]][0]=reg[u[1]][1]    
#     else:
#         print("Wrong Syntax")
#         return
#     op+=u[2]
def typeD(u):
    op=""
    # temp=bin(int(u[2]))
    if(u[0]=="ld"):
        op+="00100"
    if(u[0]=="st"):
        op+="00101"
    op=op+reg[u[1]][0]
    # temp=temp[2:]
    if len(u[2])<8:
        u[2]=u[2].rjust(8,"0")
    op=op+u[2]
    return(op)

def typeE(u):
    op=""
    temp_bin=""
    # temp=int(u[1], 2)
    ac=reg["FLAGS"][1]
    if(u[0]=="jmp"):
        op+="01111000"
        # pc=temp
    elif(u[0]=="jlt"):
        op+="10000000"
        # if(ac[-3]=='1'):
        # pc=temp
    elif(u[0]=="jgt"):
        op+="10001000"
        # if(ac[-2]=='1'):
            # pc=temp
    elif(u[0]=="je"):
        op+="10010000"
        # if(ac[-1]=='1'):
            # pc=temp
    temp_bin=bin(u[1])
    temp_bin=temp_bin[2:]
    temp_bin=temp_bin.rjust(8, "0")
    op+=temp_bin
    return(op)

def typeF(u):
    op="1001100000000000"
    return(op)

var_add={"00110011":["1"*16, "X"]}
pc=0

# for i in range(0, 2):
#     u=list(input().split())
#     print(label_check(u))

# print("The End")