def pr(pc, reg):
        print(bin(pc)[2:].rjust(8, "0"), end=" ")
        for i in reg.keys():
            #if i!="111":
                print(reg[i],end=" ")
            # elif i=="111":
            #     print(reg[i])
        print()


def pc_upd():
    global pc_cont
    global pc
    if(pc_cont==1):
        pc_cont=0
        return
    else:
        pc+=1

lst=[]
pc=0
halted=False
pc_cont=0

reg={"000":"0"*16, "001":"0"*16, "010":"0"*16, "011":"0"*16, "100":"0"*16, "101":"0"*16, "110":"0"*16, "111":"0"*16}
typeA=["00000", "00001", "00110", "01010", "01011", "01100"]
typeB=["00010", "01000", "01001"]
typeC=["00011", "00111", "01101", "01110"]
typeD=["00100", "00101"]
typeE=["01111", "10000", "10001", "10010"]
typeF=["10011"]

mem=["0"*16]*256

def func_A(line):
    reg["111"]="0"*16
    reg_1=line[7:10]
    reg_2=line[10:13]
    reg_3=line[13:16]
    val_1=int(reg[reg_1], 2)
    val_2=int(reg[reg_2], 2)
    val_3=int(reg[reg_3], 2)
    if(line[0:5]=="00000"):
        val_1=val_2+val_3
        if(val_1>65535):
            reg["111"]="0000000000001000"
            val_1=val_1%65536
    elif(line[0:5]=="00001"):
        val_1=val_2-val_3
        if(val_1<0):
            reg["111"]="0000000000001000"
            val_1=0
    elif(line[0:5]=="00110"):
        val_1=val_2*val_3
        if(val_1>65535):
            reg["111"]="0000000000001000"
            val_1=val_1%65536
    elif(line[0:5]=="01010"):
        val_1=val_2^val_3
    elif(line[0:5]=="01011"):
        val_1=val_2|val_3
    elif(line[0:5]=="01100"):
        val_1=val_2&val_3
    reg[reg_1]=bin(val_1)[2:].rjust(16, "0")

def func_B(line):
    reg["111"]="0"*16
    reg_1=line[5:8]
    val_1=reg[reg_1]
    if(line[0:5]=="00010"):
        reg[reg_1]=line[8:].rjust(16,"0")
    elif(line[0:5]=="01000"):
        temp=int(line[8:], 2)
        val_1=("0"*temp)+val_1
        reg[reg_1]=val_1[:16]
    elif(line[0:5]=="01001"):
        temp=int(line[8:], 2)
        val_1=val_1+("0"*temp)
        reg[reg_1]=val_1[-16:]

def func_C(line):
    reg_1=line[10:13]
    reg_2=line[13:16]
    val_1=int(reg[reg_1], 2)
    val_2=int(reg[reg_2], 2)
    if line[0:5]=="00011":
        reg[reg_1]=reg[reg_2]
        reg["111"]="0"*16
    elif line[0:5]=="00111":
        quo=val_1//val_2
        reg["000"]=bin(quo)[2:].rjust(16, "0")
        rem=val_1%val_2
        reg["001"]=bin(rem)[2:].rjust(16, "0")
        reg["111"]="0"*16
    elif line[0:5]=="01101":
        temp=65535
        val_2=int(reg[reg_2], 2)
        reg[reg_1]=bin(temp^val_2)[2:].rjust(16, "0")
        reg["111"]="0"*16
    elif line[0:5]=="01110":
        if val_1>val_2:
            reg["111"]="0"*14+"10"
        elif val_1<val_2:
            reg["111"]="0"*13+"100"
        elif val_1==val_2:
            reg["111"]="0"*15+"1"
    
    

def func_D(line):
    reg["111"]="0"*16
    global mem
    reg_add=line[5:8]
    mem_add=line[8:16]
    if line[0:5]=="00100":
        reg[reg_add]=mem[int(mem_add,2)]
    elif line[0:5]=="00101":
        mem[int(mem_add,2)]=reg[reg_add]

def func_E(line):
    global pc_cont
    global pc
    if(line[0:5]=="01111"):
        pc_cont=1
        pc=int(line[8:], 2)
    elif(line[0:5]=="10000"):
        if(reg["111"][-3]=='1'):
            pc_cont=1
            pc=int(line[8:], 2)
    elif(line[0:5]=="10001"):
        if(reg["111"][-2]=='1'):
            pc_cont=1
            pc=int(line[8:], 2)
    elif(line[:5]=="10010"):
        if(reg["111"][-1]=='1'):
            pc_cont=1
            pc=int(line[8:], 2)
    reg["111"]="0"*16

def func_F(line):
    global halted
    halted=True

while(True):
    line=input()
    lst.append(line)
    if(line=="1001100000000000"):
        break

while(halted==False):
    line=lst[pc]
    mem[pc]=line
    op_bin=line[0:5]
    if(op_bin in typeA):
            func_A(line)
    elif(op_bin in typeB):
            func_B(line)
    elif(op_bin in typeC):
            func_C(line)
    elif(op_bin in typeD):
            func_D(line)
    elif(op_bin in typeE):
            func_E(line)
    elif(op_bin in typeF):
            func_F(line)
    pr(pc, reg)
    pc_upd()

for i in mem:
    print(i)