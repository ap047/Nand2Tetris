import re

#Used AI for this. Made the class myself tho
class Parser: 
    import re

    def file_reader(x):
        with open(x, 'r') as file:
            asm_code = file.read()
            return asm_code.split('\n')

    def remove_comments(code):
        code = '\n'.join(code)
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code

    def remove_whitespaces(code):
        return [line.strip() for line in code.split('\n') if line.strip() != '']

    def split_lines_to_words(lines):
        return [line.split() for line in lines]

    # Example usage
    clean_code = remove_comments(file_reader('code.txt'))
    clean_code_no_whitespaces = remove_whitespaces(clean_code)
    done = split_lines_to_words(clean_code_no_whitespaces)

    #for line in final_output:
    #    print(line)

equal_counter = 0
greater_than_counter = 0
less_than_counter = 0
done_counter = 0

parsed = Parser().done

#print(parsed)

def push(x):
    return "@" + str(x) + "\n D=A \n @SP \n A=M \n M=D \n @SP \n M=M+1"

def put_back():
    return "@SP \n A=M \n M=D \n @SP \n M=M+1"

def push_local(location):
    a = "@LCL \n D=M \n @" + str(location) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_this(location):
    a = "@THIS \n D=M \n @" + str(location) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_that(location):
    a = "@THAT \n D=M \n @" + str(location) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_argument(location):
    a = "@ARG \n D=M \n @" + str(location) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_static(number):
    a = "@16 \n D=A \n @" + str(number) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_temp(number):
    a = "@5 \n D=A \n @" + str(number) + "\n A=D+A \n D=M \n" \
        + "@SP \n A=M \n M=D \n @SP \n M=M+1"
    return a

def push_pointer(number):
    a = "@" + str(number) + "\n D=A\n@3\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    return a

def pop():
    return "@SP \n AM=M-1 \n D=M"

def pop_local(location):
    a = "@LCL \n D=M \n @" + str(location) + "\n D=D+A \n @13 \n M=D \n" \
        + "@SP \n AM=M-1 \n D=M \n @13 \n A=M \n M=D"
    return a

def pop_this(location):
    a = "@THIS \n D=M \n @" + str(location) + "\n D=D+A \n @13 \n M=D \n" \
        + "@SP \n AM=M-1 \n D=M \n @13 \n A=M \n M=D"
    return a

def pop_that(location):
    a = "@THAT \n D=M \n @" + str(location) + "\n D=D+A \n @13 \n M=D \n" \
        + "@SP \n AM=M-1 \n D=M \n @13 \n A=M \n M=D"
    return a

def pop_argument(location):
    a = "@ARG \n D=M \n @" + str(location) + "\n D=D+A \n @13 \n M=D \n" \
        + "@SP \n AM=M-1 \n D=M \n @13 \n A=M \n M=D"
    return a

def pop_static(number):
    a = "@16 \n D=A \n @" + str(number) + "\n D=D+A \n @13 \n M=D \n @SP \n AM=M-1 \n" \
        + "D=M \n @13 \n A=M \n M=D"
    return a

def pop_temp(number):
    a = "@5 \n D=A \n @" + str(number) + "\n D=D+A \n @13 \n M=D \n @SP \n AM=M-1 \n" \
        + "D=M \n @13 \n A=M \n M=D"
    return a

def pop_pointer(number):
    a = "@" + str(number) + "\n D=A\n@3\nD=D+A\n@13\nM=D\n@SP\nAM=M-1\nD=M\n@13\nA=M\nM=D"
    return a

def add():
    return pop() + "\n @SP \n AM=M-1 \n D=D+M \n" + put_back()
def sub():
    return pop() + "\n @SP \n AM=M-1 \n D=M-D \n" + put_back()
def neg():
    return pop() + "\n @0 \n D=A-D \n" + put_back()
def eq():
    global equal_counter, done_counter
    a = pop() + "\n @SP \n A=M-1 \n" + " D=M-D \n @SP \n A=M \n M=0 \n @SP \n AM=M-1 \n" + "@equal" + str(equal_counter)
    b = a + "\nD;JEQ \n" + push(0) + "\n@Done" + str(done_counter) + "\n0;JMP"
    c = b + "\n(equal" + str(equal_counter) + ")\n" + "D=-1 \n" + put_back() + "\n(Done" + str(done_counter)+")"
    equal_counter+=1
    done_counter+=1
    return c
def gt(): 
    global greater_than_counter, done_counter
    a = pop() + "\n @SP \n A=M-1 \n" + " D=D-M \n @SP \n A=M \n M=0 \n @SP \n AM=M-1 \n" + "@greater" + str(greater_than_counter)
    b = a + "\nD;JLT \n" + push(0) + "\n@Done" + str(done_counter) + "\n0;JMP"
    c = b + "\n(greater" + str(greater_than_counter) + ")\n" + "D=-1 \n" + put_back() + "\n(Done" + str(done_counter)+")"
    greater_than_counter+=1
    done_counter+=1
    return c    
def lt(): 
    global less_than_counter, done_counter
    a = pop() + "\n @SP \n A=M-1 \n" + " D=D-M \n @SP \n A=M \n M=0 \n @SP \n AM=M-1 \n" + "@lesser" + str(less_than_counter)
    b = a + "\nD;JGT \n" + push(0) + "\n@Done" + str(done_counter) + "\n0;JMP"
    c = b + "\n(lesser" + str(less_than_counter) + ")\n" + "D=-1 \n" + put_back() + "\n(Done" + str(done_counter)+")"
    less_than_counter+=1
    done_counter+=1
    return c
def and_op():
    a = pop() + "\n @SP \n AM=M-1 \n D=D&M \n" + put_back()
    return a
def or_op():
    a = pop() + "\n @SP \n AM=M-1 \n D=D|M \n" + put_back()
    return a
def not_op():
    a = pop() + "\n D=!D \n" + put_back()
    return a

def checkParsed(parsed):
    cleaned_code = ''
    for i in range(len(parsed)): 
        temp = ''.join(parsed[i])
        if ("constant" in temp) and ("push" in temp): 
            cleaned_code = cleaned_code + "\n" + push(parsed[i][2])
            parsed[i] = push(parsed[i][2])
            #print(parsed[i])
            print("constant push")
        elif "add" in temp: 
            cleaned_code = cleaned_code + "\n" + add()
            parsed[i] = add()
            print("add")
        elif "sub" in temp: 
            cleaned_code = cleaned_code + "\n" + sub()
            parsed[i] = sub()
            print("sub")
        elif "lt" in temp: 
            cleaned_code = cleaned_code + "\n" + lt()
            parsed[i] = lt()
            print("less than")
        elif "neg" in temp:
            cleaned_code = cleaned_code + "\n" + neg()
            parsed[i] = neg()
            print("negative")
        elif "gt" in temp: 
            cleaned_code = cleaned_code + "\n" + gt()
            parsed[i] = gt()
            print("greater than")
        elif "eq" in temp: 
            cleaned_code = cleaned_code + "\n" + eq()
            parsed[i] = eq()
            print("eq")
        elif "and" in temp: 
            cleaned_code = cleaned_code + "\n" + and_op()
            parsed[i] = and_op()
            print("and")
        elif "or" in temp: 
            cleaned_code = cleaned_code + "\n" + or_op()
            parsed[i] = or_op()
            print("or")
        elif "not" in temp: 
            cleaned_code = cleaned_code + "\n" + not_op()
            parsed[i] = not_op()
            print("not")
        elif "local" in temp and "push" in temp:
            cleaned_code = cleaned_code + "\n" + push_local(parsed[i][2])
            parsed[i] = push_local(parsed[i][2])
            print("push local")
        elif "local" in temp and "pop" in temp:  
            cleaned_code = cleaned_code + "\n" + pop_local(parsed[i][2])
            parsed[i] = pop_local(parsed[i][2])
            print("pop local")
        elif "static" in temp and "push" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + push_static(parsed[i][2])
            parsed[i] = push_static(parsed[i][2])
            print("push static")
        elif "temp" in temp and "push" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + push_temp(parsed[i][2])
            parsed[i] = push_temp(parsed[i][2])
            print("push temp")
        elif "static" in temp and "pop" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_static(parsed[i][2])
            parsed[i] = pop_static(parsed[i][2])
            print("pop static")
        elif "temp" in temp and "pop" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_temp(parsed[i][2])
            parsed[i] = pop_temp(parsed[i][2])
            print("pop temp")
        elif "this" in temp and "push" in temp:
            cleaned_code = cleaned_code + "\n" + push_this(parsed[i][2])
            parsed[i] = push_this(parsed[i][2])
            print("push this")
        elif "that" in temp and "push" in temp:
            cleaned_code = cleaned_code + "\n" + push_that(parsed[i][2])
            parsed[i] = push_that(parsed[i][2])
            print("push that")
        elif "argument" in temp and "push" in temp:
            cleaned_code = cleaned_code + "\n" + push_argument(parsed[i][2])
            parsed[i] = push_argument(parsed[i][2])
            print("push argument")
        elif "this" in temp and "pop" in temp: 
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_this(parsed[i][2])
            parsed[i] = pop_this(parsed[i][2])
            print("pop this")
        elif "that" in temp and "pop" in temp: 
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_that(parsed[i][2])
            parsed[i] = pop_that(parsed[i][2])
            print("pop that")
        elif "argument" in temp and "pop" in temp: 
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_argument(parsed[i][2])
            parsed[i] = pop_argument(parsed[i][2])
            print("pop argument")
        elif "push" in temp and "pointer" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + push_pointer(parsed[i][2])
            parsed[i] = push_pointer(parsed[i][2])
            print("push pointer")
        elif "pop" in temp and "pointer" in temp:
            print(parsed[i][2]) 
            cleaned_code = cleaned_code + "\n" + pop_pointer(parsed[i][2])
            parsed[i] = pop_pointer(parsed[i][2])
            print("pop pointer")
    return cleaned_code
    #print(parsed)
        
with open('output.txt', 'w') as file:
    file.write(checkParsed(parsed))
