from functions import typeA,typeB,typeC,typeD,typeE,typeF
valid=True
error=""
binary=""
ins=[]
hat=False
optype={
    "A":["add","sub","mul","xor","or","and"],
    "B":["mov","rs","ls"],
    "C":["mov","div","not","cmp"],
    "D":["ld","st"],
    "E":["jmp","jlt","jgt","je"],
    "F":["hlt"]
}
reg=["R0", "R1","R2","R3","R4","R5","R6","FLAGS"]
def error_find(line,var,labels,line_count):
    hat=False
    valid=True
    global binary
    global error
    ins=list(line.split())
    if(len(ins)!=0):
        # if ins[0]=="var":
        #     valid=False
        if ins[0] in optype["A"]:
            # print(ins)
            if len(ins)!=4:
                error="ERROR:Incorrect number of operands in line "+str(line_count)
                valid=False
            elif len(ins)==4 and ins[1] in reg[:-1] and ins[2] in reg[:-1] and ins[3] in reg[:-1]:
                binary=typeA(ins)
                # return
            else:
                valid=False
                error="ERROR:Invalid register names in line "+str(line_count)
                # return 
        elif ins[0] in optype["B"] and ins[2][0]=="$":
            # print(ins,ins[1] in reg,ins[2][0:1]=="$")
            if len(ins)!=3:
                error="ERROR:Incorrect number of operands in line "+str(line_count)
                valid=False
            elif ins[1] in reg[:-1] and ins[2][0:1]=="$" and int(ins[2][1:])<=2**8-1 and int(ins[2][1:])>=0: #Imm value is 8 bits, NOT 16
                binary=typeB(ins)
                # print("81")

            else:
                valid=False
                # print("82")

                error="ERROR: Invalid register name or numerical value in line "+str(line_count)
        
        elif ins[0] in optype["C"]:
            if len(ins)!=3:
                error="ERROR:Incorrect number of operands in line "+str(line_count)
                valid=False
            elif ins[0]=="mov" and (ins[1] in reg):  # Use of flags is allowed with move instruction
                binary=typeC(ins)
            elif ins[1] in reg[:-1] and ins[2] in reg[:-1] :

                binary=typeC(ins)
            else:
                valid=False
                error="ERROR:Invalid register names in line "+str(line_count)
            # pass
        elif ins[0] in optype["D"]:
            if len(ins)!=3:
                error="ERROR:Invalid number of operands in line "+str(line_count)
                valid=False
            elif ins[1] in reg[:-1] and ins[2] in var.keys():  #MA must be a variable name.
                d=[ins[0],ins[1],var[ins[2]]]  #st r1 x
                binary=typeD(d)
            else:
                valid=False
                error="ERROR:Invalid register name or illegal use of variable name in line "+str(line_count)
        
            # pass
        elif ins[0] in optype["E"]:
            if len(ins)!=2:
                error="ERROR:Invalid number of operands in line "+str(line_count)
                valid=False
            elif ins[1] in labels.keys():  ## based on assumption that error file is being called on 2nd pass, labels contains all label names
                d=ins[0],labels[ins[1]]
                binary=typeE(d)
            else:
                valid=False
                error="ERROR: use of undeclared label name in line "+str(line_count)
        elif ins[0] in optype["F"]:
            if len(ins)!=1:
                error="ERROR:Invalid number of operands in line "+str(line_count)
                valid=False
                
            binary=typeF(ins)
            hat=True
        else:
            valid=False
            error="ERROR:Invalid instruction mnemonic in line "+str(line_count)


    return (valid,binary,error,hat)