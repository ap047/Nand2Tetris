### This file translates everything from Hack assembly into binary code

#this is from bing AI
def int_to_16bit_binary(n):
    # Convert the integer to binary and remove the '0b' prefix
    binary_str = bin(n)[2:]
    # Pad the binary string with leading zeros to make it 16 bits
    return binary_str.zfill(16)

def whatType(rawHack):
    #Counter for new variables
    counter4Var = 16
    
    #Array for preprocessed lines of code
    processed_lines = []

    for line in rawHack:
        #A Instruction check
        if "@" in line:
            where = False #if X in @X is >15
            isString = True #if Y in @Y is a string var
            #first check for comparing it to dictionary
            #with all predetermined registers and addresses
            for key in reg: 
                if line == ("@" + key): 
                    line = int_to_16bit_binary(int(reg[key]))
                    where = True
                    isString = False
            #Stated in 15
            if(not where):
                try:
                    if (type(int(line[1:])) == int):
                        line = int_to_16bit_binary(int(line[1:len(line)]))
                        isString = False
                except: pass
            #stated in 21
            if(isString):
                if not(line[1:len(line)] in reg):
                    reg.update({line.replace("@", ""): counter4Var})
                    line = int_to_16bit_binary(counter4Var)
                    counter4Var+=1
                else: 
                    line = int_to_16bit_binary(reg[key])
                
            #adds line to the unprocessed array
            processed_lines.append(line)
        #If equality for if not A instruction
        else: 
            #Temporary string that is edited
            temp_int = "111ac1c2c3c4c5c6"
            if "=" in line: 
                untilequal = line.find("=")
                for key in dest:
                    #testing equality
                    if (str(key)+"=") == line[:untilequal+1]:
                        temp_int = temp_int + str(dest[key])

                #adding jump bits as zero
                temp_int = temp_int + "000"
                
                #for C instruction
                for key in comp:
                    if line[untilequal+1:] == key:
                        temp_int = temp_int.replace("c6", str(comp[key][0][5]))
                        temp_int = temp_int.replace("c5", str(comp[key][0][4]))
                        temp_int = temp_int.replace("c4", str(comp[key][0][3]))
                        temp_int = temp_int.replace("c3", str(comp[key][0][2]))
                        temp_int = temp_int.replace("c2", str(comp[key][0][1]))
                        temp_int = temp_int.replace("c1", str(comp[key][0][0]))
                        #a bit                                                                                
                        temp_int = temp_int.replace("a", str(comp[key][1]))
            #if jumping
            else: 
                temp_int = "111ac1c2c3c4c5c6000"
                #placement of semicolon
                untilsemi = line.find(";")
                #var for condition check
                temp_before_semi = ""
                for i in range(untilsemi):
                    temp_before_semi = temp_before_semi + line[i]
                #print(temp_before_semi)
                #c bits
                for key in comp: 
                    if key == temp_before_semi:
                        temp_int = temp_int.replace("c6", str(comp[key][0][5]))
                        temp_int = temp_int.replace("c5", str(comp[key][0][4]))
                        temp_int = temp_int.replace("c4", str(comp[key][0][3]))
                        temp_int = temp_int.replace("c3", str(comp[key][0][2]))
                        temp_int = temp_int.replace("c2", str(comp[key][0][1]))
                        temp_int = temp_int.replace("c1", str(comp[key][0][0]))
                        temp_int = temp_int.replace("a", str(comp[key][1]))
                #everything after semi colon    
                temp_after_semi = ""
                for i in range(untilsemi+1, len(line)):
                    temp_after_semi = temp_after_semi + line[i]
                #print(temp_after_semi)
                keyinjmp = False
                for key in jmp:
                    #if the key we are looking at is the same as what is after 
                    #the semicolon
                    if key == temp_after_semi:
                        keyinjmp = True
                        temp_int = temp_int + (str(jmp[key][0]))
                        temp_int = temp_int + (str(jmp[key][1]))
                        temp_int = temp_int + (str(jmp[key][2]))
                if not keyinjmp:
                    temp_int = temp_int + "000"
                #print(temp_int)
            line = temp_int
            processed_lines.append(line)

    #cleans up the code
    cleaned_code = '\n'.join(processed_lines)

    return cleaned_code
   
reg = {
  "R0": "0",
  "R1": "1",
  "R2": "2",
  "R3": "3",
  "R4": "4",
  "R5": "5",
  "R6": "6",
  "R7": "7",
  "R8": "8",
  "R9": "9",
  "R10": "10",
  "R11": "11",
  "R12": "12",
  "R13": "13",
  "R14": "14",
  "R15": "15",
  "0": "0",
  "1": "1",
  "2": "2",
  "3": "3",
  "4": "4",
  "5": "5",
  "6": "6",
  "7": "7",
  "8": "8",
  "9": "9",
  "10": "10",
  "11": "11",
  "12": "12",
  "13": "13",
  "14": "14",
  "15": "15",
  "SCREEN": "16384",
  "KBD": "24576",
  "SP": "0",
  "LCL": "1",
  "ARG": "2",
  "THIS": "3",
  "THAT": "4",
}   
        
dest = {
  "M": "001",
  "D": "010",
  "DM": "011",
  "MD": "011",
  "A": "100",
  "AM": "101",
  "AD": "110",
  "ADM": "111"
}
    
comp = {
    "0": ["101010", "0"],
    "1": ["111111", "0"],
    "-1": ["111010", "0"],
    "D": ["001100", "0"],
    "A": ["110000", "0"],
    "!D": ["001101", "0"],
    "!A": ["110001", "0"],
    "-D": ["001111", "0"],
    "-A": ["110011", "0"],
    "D+1": ["011111", "0"],
    "A+1": ["110111", "0"],
    "D-1": ["001110", "0"],
    "A-1": ["110010", "0"],
    "D+A": ["000010", "0"],
    "D-A": ["010011", "0"],
    "A-D": ["000111", "0"],
    "D&A": ["000000", "0"],
    "D|A": ["010101", "0"],
    
    "M": ["110000", "1"],
    "!M": ["110001", "1"],
    "-M": ["110011", "1"],
    "M+1": ["110111", "1"],
    "M-1": ["110010", "1"],
    "D+M": ["000010", "1"],
    "D-M": ["010011", "1"],
    "M-D": ["000111", "1"],
    "D&M": ["000000", "1"],
    "D|M": ["010101", "1"],
}

jmp = {
  "JGT": "001",
  "JEQ": "010",
  "JGE": "011",
  "JLT": "100",
  "JNE": "101",
  "JLE": "110",
  "JMP": "111"
}   
from Parser import removeStuff, ASM_reader

hack = ASM_reader('Mult.asm')

#print(whatType(removeStuff(hack, reg)))

with open('output.txt', 'w') as file:
    file.write(whatType(removeStuff(hack, reg)))

#print(reg)