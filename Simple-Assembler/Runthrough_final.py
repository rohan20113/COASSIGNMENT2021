
import erroys


count_of_var=0
line_count=0
prog_counter=0
halt=False
binr=[]
vari=True #this will become false once we encounter an insruction
l=[] #list of errors
var={} # dictionary of variables along wwith the line jha unhe memory allocate ho rhi h
lab_st={} # labels ki list along with konsi line me h vo
f=[]
def label_check(u):
    if(u[0][-1]!=':'):
        return False
    else:
        temp=u[0][:-1]
        exam=["add","sub","mul","xor","or","and","mov","rs","ls","mov","div","not","cmp","ld","st","jmp","jlt","jgt","je","hlt","R0", "R1","R2","R3","R4","R5","R6","FLAGS"]
        if(temp in exam):
            return False
        if(temp.isalnum()==True):
            return True
        else:
            for i in temp:
                t=ord(i)
                if((t not in range (48, 58)) and (t not in range (65, 91)) and (t not in range (97, 123)) and (t!=95)):
                    return False
            return True
def onepass():
    global prog_counter
    global line_count
    global vari
    hl=False
    while True:

        try:
            line=input()
        except  EOFError:
           
            break
        else:
            ins=line.split()
            if len(ins)!=0:
                f.append(line)
                if ins[0]=="var" and not vari:
                    l.append("Error:variable declaration in middle of file "+str(line_count+1))
                if ins[0]=="var" and vari:
                    if(len(ins)<1 or len(ins)>2 or ins[1].isalnum()==False):
                        l.append("Invalid variable declaration in line "+str(line_count+1))
                    var[ins[1]]=-1
                elif ins[0][-1]==":" and label_check(ins): 
                    if len(ins)==1:
                        l.append("ERROR:Incomplete declaration of label in line "+str(line_count+1))
                    elif ins[0][:-1] in lab_st.keys():
                        l.append("ERROR: Multiple declaration of same label in line "+str(line_count+1))
                    else:
                        lab_st[ins[0][:-1]]=prog_counter
                    vari=False
                    prog_counter+=1
                elif ins[0][-1]==":" and not label_check(ins): 
                    l.append("Error:label is incorrect in line "+str(line_count+1) )
                else:
                    vari=False
                    prog_counter+=1
                line_count+=1
            if len(ins)==0:
                line_count+=1
                continue
            line=line.lstrip()
            line=line.rstrip()

onepass()
for item in var.keys():
    b=bin(prog_counter)
    b=b[2:]
    var[item]=b
    prog_counter+=1

for name in var.keys():
    if name in lab_st.keys():
        print("ERROR: Same name being used for variables and labels")
        exit()
line_count=0
def secondpass():
    global l
    # temp=f[-1].split(" ")
    # if "hlt" not in temp:
    #     l.append("ERROR: Missing hlt statement")
    line_count=0
    for line in f:
        line_count+=1
        if line!="\n" and line!="":
            
            fp=line.split()
            if fp[0]=="var":
            
                continue
            if label_check(fp):
                fp=fp[1:]
                line=" ".join(fp)
            tup=erroys.error_find(line,var,lab_st,line_count) # this will be a separate file which will return if the instruction is valid if not then the corresponding error also

            valid=tup[0]
            binary=tup[1]
            error=tup[2]
            if valid:
                binr.append(binary)
        
            else:
                l.append(error)
                # break
            if tup[3]==True :
                # print(line_count,len(f))
                if line_count<len(f):
                    # print("erros")
                    l.append("ERROR:hlt not being used as last instruction only"+" "+str(line_count))
                if line_count==len(f):
                    if "hlt" in f[:-1]:
                        l.append("ERROR:multiple declaration of hlt in line "+str(line_count))
                # break
            if tup[3]==False:
                if line_count==len(f):
                    l.append("ERROR:missing hlt Statement")
    
secondpass()
temp=f[-1].split(" ")
if temp[0]=="var":
    l.append("ERROR: Missing hlt statement")
if len(l)==0:
    for i in binr:
        print(i)
else:
    for i in l:
        print(i)


# LOOK into HALT and IMPORT
