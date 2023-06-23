#Dictionary for storing the instruction types and corresponding opcodes

instruction_dict = {"add":["10000", "A"], "sub":["10001", "A"], "mov":{"B":"10010","C":"10011"},
"ld":["10100", "D"], "st":["10101", "D"], "mul":["10110", "A"], "div":["10111", "C"], "rs":["11000", "B"], "ls":["11001", "B"], "xor":["11010", "A"], "or":["11011","A"],"and":["11100","A"],"not":["11101","C"],
"cmp":["11110", "C"], "jmp":["11111", "E"], "jlt":["01100", "E"], "jgt":["01101", "E"], "je":["01111", "E"], "hlt":["01010", "F"],"addf":['00000','A'],"subf":['00001','A'],"movf":['00010','B']}

#Dictionary for storing the register names and corresponding codes
register_dict={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#This is a list which stores the machine code corresponding to each insruction line
output=[]

def immToBin(N):
    N=int(N[1:])
    binary=""
    while N>0:
        rem=N%2
        binary+=str(rem)
        N//=2
    binary= binary[::-1]
    nbit = len(binary)
    binary = "0"*(8-nbit) + binary
    return binary

def floatTObinary(num): # 0.5 to binary after point wala
    if(num==0):
        return "0"
    string=""
    count=0
    while int(num)!=float(num):
        num=(num-int(num))*2
        string+=str(int(num))
        count+=1
    if(count<=5):
        return string
    else:
        return "error"

def decimalTObinary(num): #1 to binary
    string=""
    while(num!=0):
        rem=num%2
        string+=str(rem)
        num//=2
    return string[::-1]

def exponent(string):
    count=0
    for i in string:
        if i==".":
            break
        count+=1
    return count-1

def mantissa(string):
    mantissa = string[1:]
    abc = ""
    for i in mantissa:
        if(i!="."):
            abc= abc +i
    mantissa = abc
    return mantissa

def make(exp, mantissa): #generates the 16 bit value , exp is a decimal, mantissa is binary
    string= ""
    string+=format(exp, '03b')
    #print(string)
    if(len(mantissa)<5):
        string+=mantissa
        string+="0"*(5-len(mantissa))
        return string
    elif(len(mantissa)==5):
        return string+mantissa
    else:
        return "Error"
        exit()

def makefinal(num):

    fpart = floatTObinary(num - int(num))
    dpart = decimalTObinary(int(num))

    abc = dpart + "." + fpart

    m = mantissa(abc)
    exp = exponent(abc)
    
    return make(exp,m)

#These are functions for returning the machine codes for the corresponding instruction line
def add(reg1, reg2, reg3):
    output.append(instruction_dict["add"][0]+"00"+register_dict[reg1]+register_dict[reg2]+register_dict[reg3])
    return output

def addf(reg1, reg2, reg3):
    output.append(instruction_dict["addf"][0]+"00"+register_dict[reg1]+register_dict[reg2]+register_dict[reg3])
    return output

def movC(reg1, reg2):
    output.append(instruction_dict["mov"]["C"]+"00000"+register_dict[reg1]+register_dict[reg2])
    return output

def mul(reg1, reg2, reg3):
    output.append(instruction_dict["mul"][0]+"00"+register_dict[reg1]+register_dict[reg2]+register_dict[reg3])
    return output

def ls(reg1, imm):
    immBin=immToBin(imm)
    output.append(instruction_dict["ls"][0]+register_dict[reg1]+immBin)
    return output

def and_(reg1, reg2, reg3):
    output.append(instruction_dict["and"][0]+"00"+register_dict[reg1]+register_dict[reg2]+register_dict[reg3])
    return output

def jmp(mem_addr):
    output.append(instruction_dict["jmp"][0]+"000"+str(labels_dict[mem_addr]))
    return output

def je(mem_addr):
    output.append(instruction_dict["je"][0]+"000"+str(labels_dict[mem_addr]))
    return output

def movImm(reg1,imm):
    imm = immToBin(imm)
    output.append(instruction_dict["mov"]["B"]+register_dict[reg1]+imm)
    return

def movf(reg1,imm):
    imm = imm[1:]
    imm = makefinal(float(imm)) #Convert to 3 exp, 5 mantissa
    output.append(instruction_dict["movf"][0]+register_dict[reg1]+imm)
    return

def st(reg1,mem_addr):
    output.append(instruction_dict["st"][0]+register_dict[reg1]+variables_dict[mem_addr])
    return
    
def rs(reg1,imm):
    imm = immToBin(imm)
    output.append(instruction_dict["rs"][0]+register_dict[reg1]+imm)
    return

def or_(reg1,reg2,reg3):
    output.append(instruction_dict["or"][0]+"00"+register_dict[reg1]+register_dict[reg2]+register_dict[reg3])
    return

def cmp(reg1,reg2):
    output.append(instruction_dict["cmp"][0]+"00000"+register_dict[reg1]+register_dict[reg2])
    return

def jgt(mem_addr):
    output.append(instruction_dict["jgt"][0]+"000"+str(labels_dict[mem_addr]))
    return

def sub(reg1,reg2,reg3):
    output.append(instruction_dict["sub"][0] + "00" + register_dict[reg1] + register_dict[reg2] + register_dict[reg3])
    return output

def subf(reg1,reg2,reg3):
    output.append(instruction_dict["subf"][0] + "00" + register_dict[reg1] + register_dict[reg2] + register_dict[reg3])
    return output

def div(reg3,reg4):
    output.append(instruction_dict["div"][0] + "00000" + register_dict[reg3] + register_dict[reg4])
    return output

def xor(reg1,reg2,reg3):
    output.append(instruction_dict["xor"][0] + "00" + register_dict[reg1] + register_dict[reg2] + register_dict[reg3])
    return output

def not_(reg1,reg2):
    output.append(instruction_dict["not"][0] + "00000" + register_dict[reg1] + register_dict[reg2])
    return output

def jlt(mem_addr):
    output.append(instruction_dict["jlt"][0]+"000"+ str(labels_dict[mem_addr]))
    return output

def ld(reg1,mem_addr):
    output.append(instruction_dict["ld"][0] + register_dict[reg1] + variables_dict[mem_addr])
    return output

def hlt():
    output.append(instruction_dict["hlt"][0] + 11*"0")
    return output

#These are the functions for checkinng error specific to a certain instruction type
def checkTypeAError(instructList):
    error=[]
    if(len(instructList)!=4):
        error.append("Invalid Syntax")
        return [True, error]
    if(instructList[0] not in instruction_dict.keys()):
        error.append("Not a valid instruction")
        return [True, error]
    elif(instructList[1] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    elif(instructList[2] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    elif(instructList[3] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    else:
        return [False]
    
def checkTypeBError(instructList):
    error=[]
    if(len(instructList)!=3):
        error.append("Invalid Syntax")
        return [True, error]
    if(instructList[0] not in instruction_dict.keys()):
        error.append("Not a valid instruction")
        return [True, error]
    elif(instructList[1] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    # elif("." in instructList[2][1:]):
    #     error.append("Not a valid immediate value")
    #     return [True, error]
    elif(instructList[0]=="mov" and (int((instructList[2][1:]))>255 or int(instructList[2][1:])<0)):
        error.append("Not a valid immediate value")
        return [True, error]
    # elif(instructList[0]=="movf" and (float((instructList[2][1:]))>252 or (float(instructList[2][1:])<1))):
    #     print("2")
    #     error.append("Not a valid immediate value")
    #     return [True, error]
    else:
        return [False]
    
def checkTypeCError(instructList):
    error=[]
    if(len(instructList)!=3):
        error.append("Invalid Syntax")
        return [True, error]
    if(instructList[0] not in instruction_dict.keys()):
        error.append("Not a valid instruction")
        return [True, error]
    elif(instructList[1] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    elif (instructList[2] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    else:
        return [False]

def checkTypeDError(instructList):
    error=[]
    if(len(instructList)!=3):
        error.append("Invalid Syntax")
        return [True, error]
    if(instructList[0] not in instruction_dict.keys()):
        error.append("Not a valid instruction")
        return [True, error]
    elif(instructList[1] not in register_dict.keys()):
        error.append("Not a valid register name")
        return [True, error]
    elif(instructList[2] not in variables):
        error.append("The Variable is not defined")
        return [True, error]
    else:
        return [False]

def checkTypeEError(instructList):
    error=[]
    if(len(instructList)!=2):
        error.append("Invalid Syntax")
        return [True, error]
    if(instructList[0] not in instruction_dict.keys()):
        error.append("Not a valid instruction")
        return [True, error]
    elif(instructList[1] not in labels):
        error.append("Not a valid label name")
        return [True, error]
    else:
        return [False]

instructions=[] #List which will contain each instruction as a nested list
labels=[] #List of labels
variables=[] #List of variables
labels_dict={} #Stores key value pairs as "label name": "mem_addr"
variables_dict = {} #Stores key value pairs as "variable name": "mem_addr"
j=0
while True:
    try:
        instruct=input().strip()
        instructList=instruct.split()
        if instruct=="": #Checking for empty line
            continue
        elif instructList[0][-1]==":": #Checking for labels
            if (instructList[0][:-1] not in register_dict and instructList[0][:-1] not in instruction_dict):
                labels_dict[instructList[0][:-1]]=immToBin("$"+str(j-len(variables)))
                labels.append(instructList[0][:-1])
                instructList.pop(0)
        elif instructList[0]=="var": #Checking for variable declaration
            variables.append(instructList[1])
        instructions.append(instructList)
        j+=1
    except EOFError: #If taking input has ended(ctrl+D is pressed)
        break
    except:
        continue

#Now we are checking for specific errors

for i in range(0, len(labels)):
    if labels.count(labels[i])>1:
        print("Error: Multiple labels declared with the same name")
        exit()

flag=0
for i in range(0, len(instructions)):
    for j in instructions[i]:
        if (j=="hlt"):
            flag=1
            break
if(flag==0):
    print("Error:", end=" ")
    print("Missing hlt instruction")
    exit()

if(instructions[len(instructions)-1][0]!="hlt"):
    print("Error @ line", len(instructions), "hlt has not been used as the last instruction")
    exit()

if(instructions[len(instructions)-1][0]=="hlt"):
    if(instructions[len(instructions)-1][0]!=instructions[len(instructions)-1][-1]):
        print("Error @ line", len(instructions), "Invalid Syntax")
        exit()

for i in range(0, len(instructions)):
        instructions[i][0]
        if(instructions[i][0]!="var" and instructions[i][0] not in instruction_dict.keys()):
            print("Error @Line", i+1, "Not a valid instruction")
            exit()

#Assigning mem_addr to variables
varmem = len(instructions) - len(variables)
for i in variables:
    if i not in variables_dict.keys():
        variables_dict[i]=immToBin("$"+str(varmem))
        varmem+=1

hltCount=0
for i in range(0, len(instructions)):
    for j in instructions[i]:
        if j=="hlt":
            hltCount+=1
if(hltCount>1):
    print("Error:", end=" ")
    print("Multiple hlt instructions used")
    exit()

for i in range(0,len(instructions)):
    if(instructions[i][0][-1]==":" and len(instructions[i])==1):
        print("Error @Line "+str(i+1)+" No instruction found after label")
        exit()

for i in range(len(variables),len(instructions)):
    if( "var" == instructions[i][0]):
        print("Error @Line "+str(i+1)+" Variable should be defined at the beginning")
        exit()
for i in range(0,len(instructions)):
    if("FLAGS" in instructions[i]):
        if(instructions[i][0]!="mov"):
            print("Error @Line "+str(i+1)+" Illegal use of FLAGS")
            exit()
for i in range(0,len(instructions)):
    if(instructions[i][0] in ["ld","st"]):
        if(instructions[i][2] not in variables):
            print("Error @Line "+str(i+1)+" Undefined Variable")
            exit()
for i in variables:
    if(i in labels):
        repeated = i
        break
for i in range(0,len(instructions)):
    if(instructions[i][0]=="repeated"+":"):
        print("Error @Line "+str(i+1)+" Misuse of label")
        exit()        
for i in range(0,len(instructions)):
    if(instructions[i][0] in ["jmp","jlt","jgt","je"] and instructions[i][1] not in labels):
        print("Error @Line "+str(i+1)+" Undefined Label")
        exit()   

for i in range(0, len(instructions)):
    label_count=0
    for j in instructions[i]:
        if (j[-1]==":"):
            label_count+=1
    if(label_count>1):
        print("Error @ line", i, "Multiple labels in the same line")
        exit()

for i in range(0, len(instructions)):
    for j in instructions[i]:
        if(j[-1]==":"):
            if(j[:-1] in instruction_dict):
                print("Error @ line", i+1, "Cannot use instructions as label names")
                exit()
            if(j[:-1] in register_dict):
                print("Error @ line", i+1, "Cannot use register names as label names")
                exit()

flag=True
for i in range(0,len(instructions)):
    if(instructions[i][0]=="add"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="sub"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="addf"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="subf"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="movf"):
        if(checkTypeBError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeBError(instructions[i])[1][0])
            exit()
        imm = makefinal(float(instructions[i][2][1:]))
        if(imm == "Error"):
            print("Error @Line", i+1,"Not a valid immediate value")
            exit()
        if("." not in instructions[i][2]):
            print("Error @Line", i+1,"Value given is not float")
            exit()
        if(float(instructions[i][2][1:])<1):
            print("Error @Line", i+1,"Value cannot be stored in the given format")
            exit()
    if(instructions[i][0]=="mul"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="xor"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="or"):
        if(checkTypeAError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeAError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="mov" and (instructions[i][2] not in register_dict.keys() and instructions[i][2][0]!="$")):
        print("Error @Line", i+1, "General Syntax Error")
        exit()
    if(instructions[i][0]=="mov" and instructions[i][2][0]=="$"):
        if(checkTypeBError(instructions[i])[0]==True):
           flag=False
           print("Error @Line", i+1, end=" ")
           print(checkTypeBError(instructions[i])[1][0])
           exit()
    if(instructions[i][0]=="ls"):
        if(checkTypeBError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeBError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="rs"):
        if(checkTypeBError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeBError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="mov" and instructions[i][2] in register_dict.keys()):
        if(checkTypeCError(instructions[i])[0]==True):
           flag=False
           print("Error @Line", i+1, end=" ")
           print(checkTypeCError(instructions[i])[1][0])
           exit()
    if(instructions[i][0]=="not"):
        if(checkTypeCError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeCError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="cmp"):
        if(checkTypeCError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeCError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="ld"):
        if(checkTypeDError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeDError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="st"):
        if(checkTypeDError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeDError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="jmp"):
        if(checkTypeEError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeEError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="jlt"):
        if(checkTypeEError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeEError(instructions[i])[1][0])
            exit()
    if(instructions[i][0]=="jgt"):
        if(checkTypeEError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeEError(instructions[i])[1][0])
            exit()
    elif(instructions[i][0]=="je"):
        if(checkTypeEError(instructions[i])[0]==True):
            flag=False
            print("Error @Line", i+1, end=" ")
            print(checkTypeEError(instructions[i])[1][0])
            exit()
    if(instructions[i][0][-1]==":"):
        continue
    if(instructions[i][0]=="var"):
        continue
    if(instructions[i][0] not in instruction_dict):
        print("Error @ Line", i+1, "Not a valid instruction")
        exit()

if flag==True:
  PC=0
  while(PC<len(instructions)):
      if(instructions[PC][0]=="add"):
          add(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="addf"):
          addf(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="sub"):
          sub(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="subf"):
          subf(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="mov" and instructions[PC][2] in register_dict.keys()):
            movC(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="mov" and instructions[PC][2][0]=="$"):
            movImm(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="movf"):
            movf(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="ld"):
          ld(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="st"):
          st(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="mul"):
          mul(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="div"):
          div(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="ls"):
          ls(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="rs"):
          rs(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="xor"):
          xor(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="or"):
          or_(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="and"):
          and_(instructions[PC][1],instructions[PC][2],instructions[PC][3])
      if(instructions[PC][0]=="not"):
          not_(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="cmp"):
          cmp(instructions[PC][1],instructions[PC][2])
      if(instructions[PC][0]=="jmp"):
          jmp(instructions[PC][1])
      if(instructions[PC][0]=="jlt"):
          jlt(instructions[PC][1])
      if(instructions[PC][0]=="jgt"):
          jgt(instructions[PC][1])
      if(instructions[PC][0]=="je"):
          je(instructions[PC][1])
      if(instructions[PC][0]=="hlt"):
          hlt()  
      PC=PC+1

for i in output:
    print(i)
