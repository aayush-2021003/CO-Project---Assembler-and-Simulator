#Simulator Q4
import sys
import matplotlib.pyplot as plt



RegDict={"000":"0000000000000000","001":"0000000000000000","010":"0000000000000000",              
        "011":"0000000000000000","100":"0000000000000000","101":"0000000000000000",
        "110":"0000000000000000","111":"0000000000000000"}

MemoryDumpList = []
x = []
y = []
cycle = 1
i =0
while(i<256):
    line = input()
    line.strip()
    MemoryDumpList.append(line)
    i+=1
    if(line == "0101000000000000"):
        break

while(i<256):
    MemoryDumpList.append("0000000000000000")
    i+=1

def floatTObinary(num):
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

def decimalTObinary(num):
    string=""
    while(num!=0):
        rem=num%2
        string+=str(rem)
        num//=2
    return string[::-1]

def binaryTOfloat(string):
    val=0
    power=-1
    for i in string:
        val+=int(i)*(2**power)
        power-=1
    return val

def exponent(string):
    count=0
    for i in string:
        if i==".":
            break
        count+=1
    return count-1

def make(exp, mantissa): #generates the 16 bit value , exp is a decimal, mantissa is binary
    string= "00000000"
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

def floatType1(inst):
    opcode=inst[0:5]
    reg1 = inst[7:10]
    reg2 = inst[10:13]
    reg3 = inst[13:16]
    if(opcode=="00000"):
        val1=(1+binaryTOfloat(RegDict[reg1][11:]))*2**int(RegDict[reg1][8:11], 2)
        #print(val1)
        val2=(1+binaryTOfloat(RegDict[reg2][11:]))*2**int(RegDict[reg2][8:11], 2)
        #print(val2)
        sum=val1+val2
        #print(sum)
        sumBinary=decimalTObinary(int(sum))+"."+floatTObinary(sum-int(sum))
        #print(sumBinary)
        exp=exponent(sumBinary)
        #print(format(exp, '03b'))
        dotidx = sumBinary.find('.')
        exp1 = dotidx-1
        mantissa = sumBinary[1:]
        abc = ""
        for i in mantissa:
            if(i!="."):
                abc= abc +i
        mantissa = abc
        if(make(exp, mantissa)=="Error"):
            RegDict[reg3]="0000000011111111"
            RegDict['111']='0000000000001000'
        else:
            RegDict[reg3]=make(exp, mantissa)
    if(opcode=="00001"):
        val1=(1+binaryTOfloat(RegDict[reg1][11:]))*2**int(RegDict[reg1][8:11], 2)
        #print(val1)
        val2=(1+binaryTOfloat(RegDict[reg2][11:]))*2**int(RegDict[reg2][8:11], 2)
        #print(val2)
        sum=val1-val2
        if(sum<1):
            RegDict[reg3]="0000000000000000"
            RegDict['111']="0000000000001000"
        else:
            #print(sum)
            sumBinary=decimalTObinary(int(sum))+"."+floatTObinary(sum-int(sum))
            #print(sumBinary)
            exp=exponent(sumBinary)
            #print(format(exp, '03b'))
            dotidx = sumBinary.find('.')
            exp1 = dotidx-1
            mantissa = sumBinary[1:]
            abc = ""
            for i in mantissa:
                if(i!="."):
                    abc= abc +i
            mantissa = abc
            if(make(exp, mantissa)=="Error"):
                RegDict[reg3]="0000000011111111"
                RegDict['111']='0000000000001000'
            else:
                RegDict[reg3]=make(exp, mantissa)

def floatType2(inst): #movf
    opcode=inst[0:5]
    reg1=inst[5:8]
    imm=inst[8:16]
    string="00000000"+imm
    RegDict[reg1]=string


#Input taking done MemoryDumpList is a list of 256 size with instructions stored first and then zeroes

def typeA(inst):
    #inst is a string which is a line of code
    opcode = inst[0:5]
    reg1 = inst[7:10]
    reg2 = inst[10:13]
    reg3 = inst[13:16]
    if(opcode=="10000"):
        x = int(RegDict[reg1],2) + int(RegDict[reg2],2)
        #print("x is: ",x)
        if(x>=2**16):
            RegDict['111'] = '0000000000001000'
            x=x%(2^16)
            RegDict[reg3] = format(x,'016b')
        else:
            RegDict[reg3] = format(x,'016b')
            RegDict['111'] = '0000000000000000'
    if(opcode=="10001"):
        x = int(RegDict[reg1],2) - int(RegDict[reg2],2)
        if(x<0):
            RegDict['111'] =  '0000000000001000'
            RegDict[reg3] = '0000000000000000'
        else:
            RegDict[reg3] = format(x,'016b')
            RegDict['111'] = '0000000000000000'
    if(opcode=="10110"):
        x = int(RegDict[reg1],2)*int(RegDict[reg2],2)
        RegDict[reg3] = format(x,'016b')
        RegDict['111'] = '0000000000000000'
    if(opcode=="11010"):
        x = int(RegDict[reg1],2)^int(RegDict[reg2],2)
        RegDict[reg3] = format(x,'016b')
        RegDict['111'] = '0000000000000000'
    if(opcode=="11011"):
        x = int(RegDict[reg1],2)|int(RegDict[reg2],2)
        RegDict[reg3] = format(x,'016b')
        RegDict['111'] = '0000000000000000'
    if(opcode=="11100"):
        x = int(RegDict[reg1],2)&int(RegDict[reg2],2)
        RegDict[reg3] = format(x,'016b')
        RegDict['111'] = '0000000000000000'

#Function for handling type B instructions
def typeB(inst):
    opcode = inst[0:5]
    reg1 = inst[5:8]
    Imm= inst[8:16]
    if(opcode=="10010"):
        x= int(Imm,2)
        RegDict[reg1] = format(x,'016b')
    if(opcode=="11001"):
        x= int(RegDict[reg1],2) << int(Imm,2)
        RegDict[reg1]= format(x,'016b')
    if(opcode=="11000"):
        x= int(RegDict[reg1],2) >> int(Imm,2)
        RegDict[reg1]= format(x,'016b')
    RegDict['111'] = '0000000000000000'

#Function for handling Type C instructions
def typeC(inst):
    opcode=inst[0:5]
    reg1=inst[10:13]
    reg2=inst[13:16]
    if(opcode=="10011"):
        RegDict[reg2]=RegDict[reg1]
        RegDict['111'] = '0000000000000000'
    if(opcode=="10111"):
        RegDict["000"]=format(int(RegDict[reg1], 2)//int(RegDict[reg2],2), '016b')
        RegDict["001"]=format(int(RegDict[reg1], 2)%int(RegDict[reg2],2), '016b')
        RegDict['111'] = '0000000000000000'
    if(opcode=="11101"):
        inverted=""
        for i in RegDict[reg1]:
            if(i=="0"):
                inverted+="1"
            if(i=="1"):
                inverted+="0"
        RegDict[reg2]=inverted
        RegDict['111'] = '0000000000000000'
    if(opcode=="11110"):
        if(int(RegDict[reg1], 2)==int(RegDict[reg2], 2)):
            RegDict["111"]="0000000000000001"
        if(int(RegDict[reg1], 2)>int(RegDict[reg2], 2)):
            RegDict["111"]="0000000000000010"
        if(int(RegDict[reg1], 2)<int(RegDict[reg2] ,2)):
            RegDict["111"]="0000000000000100"
            
#Function for handling type D instructions
def typeD(inst):
    opcode= inst[0:5]
    reg1 = inst[5:8]
    mem_addr= inst[8:16]
    idx = int(mem_addr, 2)
    if(opcode=="10100"):
        RegDict[reg1]= MemoryDumpList[idx]
    if(opcode=="10101"):
        MemoryDumpList[idx]= RegDict[reg1]
    RegDict['111'] = '0000000000000000'

#Function for handling type E instructions
def typeE(inst, pc):
    opcode=inst[0:5]
    memAddr=inst[8:16]
    if(opcode=="11111"):
        pc=int(memAddr, 2)

    if(opcode=="01100"):
        if(RegDict["111"][-3]=="1"):
            pc=int(memAddr, 2)
        else:
            pc=pc+1
    if(opcode=="01101"):
        if(RegDict["111"][-2]=="1"):
            pc=int(memAddr, 2)
        else:
            pc=pc+1
    if(opcode=="01111"):
        if(RegDict["111"][-1]=="1"):
            pc=int(memAddr, 2)
        else:
            pc=pc+1
    RegDict['111'] = '0000000000000000'
    return pc

def typeF(inst):
    RegDict['111'] = '0000000000000000'

def printLine(pc):
    print(format(pc,'08b'),end = ' ')
    for i in RegDict.values():
        print(i,end=" ")    
    print()

def memoryDump(l):
    for i in l:
        print(i)

pc = 0

while(True):
    x.append(cycle)
    y.append(pc)
    cycle += 1

    line = MemoryDumpList[pc]
    
    if(line[0:5]=='10000' or line[0:5]=='10001' or line[0:5]=='10110' or line[0:5]=='11010' or line[0:5]=='11011' or line[0:5]=='11100'):
        typeA(line)
        printLine(pc)
        pc+=1

    if(line[0:5]=='00000' or line[0:5]=='00001'):
        floatType1(line)
        printLine(pc)
        pc+=1

    if(line[0:5]=='00010'):
        floatType2(line)
        printLine(pc)
        pc+=1
    
    if(line[0:5]=='10010' or line[0:5]=='11001' or line[0:5]=='11000'):
        typeB(line)
        printLine(pc)
        pc+=1
        
    
    if (line[0:5] == '10011' or line[0:5] == '10111' or line[0:5] == '11101' or line[0:5] == '11110'):
        typeC(line)
        printLine(pc)
        pc += 1
        
    
    if (line[0:5] == '10100' or line[0:5] == '10101'):
        typeD(line)
        printLine(pc)
        pc += 1
        
    
    if(line[0:5] == '01111' or line[0:5] == '01100' or line[0:5] == '01101' or line[0:5] == '11111'):
        #print("branch")
        pctemp = pc #we store the value of pc as pc is going to change because of its global scope
        pc = typeE(line,pc) #value of pc is updated in the function
        printLine(pctemp)

    if (line[0:5] == '01010'):
        typeF(line)
        printLine(pc)
        break

memoryDump(MemoryDumpList)
plt.xlabel("Cycle Number")
plt.ylabel("Memory adress")
plt.title('My first graph')
plt.scatter(x,y)
plt.show()