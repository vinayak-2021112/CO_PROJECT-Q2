try:
    # instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
    #                 "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
    #                 "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
    #                 "je": "01111", "hlt": "01010", "var": "00000"}



    instruction = {"add": "00000", "sub": "00001", "ld": "00100", "st": "00101", "mul": "00110",
            "div": "00111", "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101",
            "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011",
            "movi":"00010","movr":"00011"
            }
    register = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110",
                "FLAGS": "111"}
    reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110"}

    flag = "0000000000000000"
    dictreg = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0}
    ErrorArray = []
    # variables
    arr = []
    line_counter = 0
    halt_count = 0
    load_store = {}
    label = {}
    variables = {}
    # reading from file
    f = open("Myfile.txt", "w")
    # f.write(str(input().split()))
    while True:
        try:
            s = input()
            if(s==''):
                continue
            s=" ".join(s.split())
            f.write(s + "\n")

        except EOFError:
            break
    f.close()
    f = open("Myfile.txt", "r")

    # extracting individual lines from file
    s = f.read().split("\n")
    s = s[:len(s) - 1]

    pcNo = len(s)
    leng_instruction = len(s)
    leng_instruction_og = len(s)
    ErrorFlag = 0
    addtoLabel = True

    def flag_str_to_int(s):
        u=0
        for i in range(len(s)):
            u+=int(s[i])*(2**(len(s)-i-1))

        return u


    def binary(n):
        s = ''
        b = 0
        while n >= 1:
            s += str(n % 2)
            n = n // 2
        return "0" * (8 - len(s)) + s[::-1]


    # def xor_or_and(s, a, b):
    #     if s == "or":
    #         return a | b
    #     if s == "xor":
    #         return a ^ b
    #     if s == "and":
    #         return a & b


    # function for flag
    # def flagfunc(a, b, flag):
    #     flag = "0000000000000000"
    #     if (a == b):
    #         flag = 15 * "0" + "1"
    #         return flag
    #     if (a > b):
    #         flag = 14 * "0" + "1" + "0"
    #         return flag
    #     elif (a < b):
    #         flag = 13 * "0" + "1" + "00"
    #         return flag


    # def add_sub_mul_xor_or_and(s, a, b):
    #     if s == "mul":
    #         if a * b < 255:
    #             return a * b  # check krna hai
    #         else:
    #             # ErrorArray.append("Underflow")
    #             return -1
    #     if s == "add":
    #         if a + b < 255:
    #             return (a + b)
    #         else:
    #             # ErrorArray.append("Overflow")
    #             return -1
    #     if s == "sub":
    #         if a - b > 0:
    #             return (a - b)
    #         else:
    #             # ErrorArray.append("Underflow")
    #             return -1
    #     if s in ["xor", "or", "and"]:
    #         return xor_or_and(s, a, b)


    # checking for labels if any
    count = 0  # change made for resolution of X problem


    def apply(i):
        global pcNo, ErrorFlag, flag, addtoLabel,leng_instruction,x,halt_count
        k = i.split(" ")
        string = ""
        if list(k[0]) == []:
            k = k[1:]
        #  print(k)
        # for u in k:
        #     if list(u) == []:
        #         ErrorArray.append(f"ERROR: Incorrect instruction Syntax at line {line_counter +1 }")
        #         ErrorFlag += 1
        #         return

        if k[0] == "var":
            try:
                assert len(k) == 2
                variables[k[1]] = leng_instruction-x
                leng_instruction+=1
            except AssertionError:
                ErrorArray.append(f"ERROR: Incorrect variable syntax at line {line_counter + 1}")
                ErrorFlag += 1
                return
        # seperate conditions for miv immediate and mov register

        # flag error handling
        if len(k) > 1:
            if "FLAGS" in k:
                try:
                    # assert k[0] == "mov" and k[2] in reg
                    # dictreg[k[2]] = flag_str_to_int(flag)
                    assert k[0] == "mov" and k[1] in reg
                    dictreg[k[1]] = flag_str_to_int(flag)
                except AssertionError:
                    ErrorArray.append(f"ERROR: Illegal use of flag register at line {line_counter + 1}")
                    ErrorFlag += 1
                    return

        if k[0] == "mov" and k[2] not in register.keys():
            try:
                assert k[2][0] == "$"
            except AssertionError:
                ErrorArray.append(f"Error: Immediate value has incorrect syntax at line {line_counter + 1}")
                ErrorFlag += 1
                return
            
            try:
                assert int(k[2][1:]) <= 255
                assert int(k[2][1:]) >=0
                string += instruction["movi"] + register[k[1]] + binary(int(k[2][1:]))
            except AssertionError:
                ErrorArray.append(f"ERROR: Illegal immediate value at line {line_counter + 1}")
                ErrorFlag += 1
                return

        if k[0] == "mov" and k[2] in register.keys():
            string += instruction["movr"] + "00000" + register[k[1]] + register[k[2]]
            

        if k[0] in ["add", "sub", "mul", "xor", "or", "and"]:
            try:
                assert len(k) >= 4
                if k[1] not in register.keys() or k[2] not in register.keys() or k[3] not in register.keys():
                    ErrorArray.append(f"ERROR: Invalid instruction syntax for {k[0]} at line  {line_counter + 1}")
                    addtoLabel = False
                    return

                string += instruction[k[0]] + "00" + register[k[1]] + register[k[2]] + register[k[3]]
                
                if k[0] in ["add", "sub", "mul"]:
                    if k[0] == ("add" or "sub" or "mul") and dictreg[k[1]] == -1:
                        flag[-3] = 1
            except AssertionError:
                ErrorArray.append(f"ERROR: Insufficient Registers at line {line_counter+1}")
                ErrorFlag += 1
                addtoLabel = False
                return

        if k[0] in ["ls", "rs"]:
            if k[1] not in reg.keys():
                ErrorArray.append(f"ERROR:Invalid instruction syntax at line {line_counter + 1}")
                ErrorFlag+=1
                return
            try:
                assert int(k[2][1:]) <= 255
                string += instruction[k[0]] + register[k[1]] + binary(int(k[2][1:]))
            except AssertionError:
                ErrorArray.append(f"ERROR: Immediate value is greater than 8 Bits at line {line_counter + 1}")
                ErrorFlag += 1
                return
        if k[0] in ["div", "not", "cmp"]:
            string += instruction[k[0]] + "00000" + register[k[1]] + register[k[2]]
            

        if k[0] in ["ld", "st"]:
            # dictreg stuff is left
            try:
                assert k[2] in variables
                if(k[2] in load_store):
                    string += instruction[k[0]] + register[k[1]] + binary(variables[k[2]])
                else:
                    load_store[k[2]] = leng_instruction-x
                    string += instruction[k[0]] + register[k[1]] + binary(variables[k[2]])
                    leng_instruction+=1
                pcNo += 1
            except AssertionError:
                ErrorArray.append(f"ERROR: Undeclared variable used at line {line_counter+1}")
                ErrorFlag+=1
        if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] in label.keys():
            string += instruction[k[0]] + "000" + label[k[1]][0]

        if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] not in label.keys():
            ErrorArray.append(f"ERROR: Invalid memory address at line {line_counter + 1}")
            ErrorFlag+=1
            return
        if k[0] == "hlt":
            halt_count+=1
            try:
                assert halt_count==1
                string += instruction[k[0]] + "00000000000"
                
            except AssertionError:
                ErrorArray.append(f"ERROR: Multiple halt instructions used")
                ErrorFlag+=1
        arr.append(string)


    def check_initial_label(i):
        global line_counter, addtoLabel, x, arr
        j = 0
        while(i[j]==" "):
            j+=1
        i = i[j:]
        
        k = i.split(" ")
        if k[0] == "mov" or k[0] == "var":
            return
        elif k[0] not in instruction.keys():
        
            if k[0][-1] == ":":
                if len(k) == 1:
                    return
                lb_len = len(k[0])
                j = 1
                while(k[j]==''):
                    
                    j = j+1
                # if (i[lb_len] == " ") and (i[lb_len + 1] != " "):
                if k[j] in instruction.keys() or k[j] == "mov":

                    d = []

                    d.append(binary(line_counter - x))
                    
                    label[i[0:lb_len-1]] = d
                    apply(str(i)[lb_len+j:])
                    
                    if addtoLabel:
                        
                        d.append(arr[-1])
                        
                        label[i[0:lb_len - 1]] = d
                        return
                else:
                    return 0
            else:
                return 0
        else:
            return 0


    x = 0

    for i in s:
        k = i.split(" ")
        if k[0]=="var":
            x=x+1

    for i in s:

        k = i.split(" ")
        if k[0] == "var":
            variables[k[1]] = 0
            
        if(ErrorFlag==0):
            check_initial_label(i)
            line_counter += 1
        else:
            break
    halt_count=0
    pcNo -= x
    line_counter = 0


    # checking if the immediate value is > 8bit

    def function(s):
        global line_counter, ErrorFlag
        for i in s:
            # check for illegal immediate value
            # immediate_check(i.split(" "))
            # will pass only the part of the string after a valid label
            if(ErrorFlag>0):
                return
            j = 0
            while(i[j]==" "):
                j+=1
            i = i[j:]
            k = i.split(" ")

            try:
                assert i.split(" ") != ['']
                j = 0
                while (i[j] == " "):
                    j += 1
                i = i[j:]
                lab_len = check_labels(str(i))
                if lab_len > 0:
                    apply(str(i)[lab_len:])
                    line_counter += 1
                elif lab_len == 0:
                    apply(str(i)[lab_len:])
                    line_counter += 1

                else:
                    # ERROR HANDLING
                    line_counter += 1
                    continue


            except AssertionError:
                ErrorArray.append(f"ERROR: Blank Line at {line_counter + 1}")
                ErrorFlag += 1




    def check_labels(i):
        global count, ErrorFlag
        j = 0
        while(i[j]==" "):
            j+=1
        i = i[j:]
        
        k = i.split(" ")
        
        if k[0] == "mov" or k[0] == "var":
            return 0
        elif k[0] not in instruction.keys():
            if k[0][-1] == ":":
                if len(k) == 1:
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: No instruction after label at line {line_counter + 1}")
                    return -1
                
                label_len = len(k[0])
                j = 1
                while(k[j]==''):
                    
                    j = j+1
            # if (i[lb_len] == " ") and (i[lb_len + 1] != " "):
                
                if k[j] in instruction.keys() or k[j] == "mov":
                    return label_len +j
                else:
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                    return -1
                
            elif len(k) != 1 and k[1] == ":":
                if k[1] == ":":
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                    return -1
                else:
                    return 0
            elif len(k)>1 :
                if k[1] in instruction.keys() or k[1]=="mov":
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                    return -1
                else:
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: Invalid instruction syntax at line {line_counter + 1}")
                    return -1

            else:
                ErrorFlag += 1
                ErrorArray.append(f"ERROR: Invalid instruction syntax at line {line_counter + 1}")
                return -1
        else:
            return 0


    arr = []
    variables={}
    leng_instruction = leng_instruction_og
    load_store = {}
    if(ErrorFlag==0):
        halt_count=0
        ErrorArray=[]
        ErrorFlag=0
        function(s)


    hltFlag = 0
    # print(x,len(s),s)

    for i in range(x, len(s)):
        #  print(i)
        try:
            assert s[i].split(" ") != ['']
            j = 0
            while (s[i][j] == " "):
                j += 1
            s[i] = s[i][j:]
            k = s[i].split(" ")

            if k[0] == "var":
                ErrorFlag += 1
                ErrorArray.append(f"ERROR: Var declared at incorrect position at line {i + 1}")

            if i == len(s) - 1:
                if k[0] != "hlt":
                    hltFlag += 1
            if i < len(s) - 1:
                if k[0] == "hlt":
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: hlt used before last instruction at line {i + 1}")
        except AssertionError:
            ErrorArray.append(f"ERROR,Blank Line at {i + 1}")
            ErrorFlag += 1

    if(len(arr)>0 and ErrorFlag==0):
        if arr[-1] == "1001100000000000":
            pass
        else:
            ErrorFlag += 1
            ErrorArray.append("ERROR: hlt not in given file")

    if ErrorFlag == 0 and len(ErrorArray)==0:
        for i in range(x, len(arr)):
            print(arr[i])
    for i in ErrorArray:
        print(i)
    f.close()
    f = open('Myfile.txt', 'w')
    f.write("")
    f.close()
except:
    print(f"ERROR: General syntax error at line {line_counter+1}")
