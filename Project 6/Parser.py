#This Parser.py file should:
#Read the file
#Break it down into fields and sumbols
#Remove white space and comments

def ASM_reader(x):
    with open(x, 'r') as file:
        asm_code = file.read()
    
    return asm_code.split('\n')

def removeStuff(rawCode, dict):
    processed_lines = []
    line_count = 0
    for line in rawCode:
        line = line.strip()  # Remove leading and trailing whitespace
        if '//' in line or ('(' in line and ')' in line):
            if not ('//' in line):
                dict.update({line.replace("(", "").replace(")", ""): line_count})
            line = ""  # Keep only the part before the comment and strip again
            
        if line:  # Only add non-empty lines
            processed_lines.append(line)
            line_count+=1
    
    #cleaned_code = '\n'.join(processed_lines)
    #return cleaned_code
    
    return processed_lines

my_dict={}

# Example usage
raw_code = ASM_reader('Mult.asm')
cleaned_code = removeStuff(raw_code, my_dict)

print((cleaned_code))
print(my_dict)


