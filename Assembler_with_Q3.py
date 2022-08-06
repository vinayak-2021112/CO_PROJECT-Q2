try:
    instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
                    "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
                    "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
                    "je": "01111", "hlt": "01010", "var": "00000","addf":"00000","subf":"00001","movf":"00010"}

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
            if (s == ''):
                continue
            s = " ".join(s.split())
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


    def to_binaryfloat(num):
        s = str(bin(num))
        binary_num = s[2:]
        if (len(binary_num) < 8):
            binary_num = (3 - len(binary_num)) * '0' + binary_num
        return binary_num


    wxx = ''
    pqr = 0


    def rec(x):
        global wxx, pqr
        s = x / (10 ** len(str(x)))
        s1 = str(s).split(".")
        pqr += 1

        if (s1[1]) == '0' or pqr > 5:
            return
        s2 = str(((int(s1[1]) * 2) / 10 ** len(str(s1[1])))).split(".")

        wxx += s2[0]

        rec(int(s2[1]))

    def funcfordecimal(x):
        global wxx,pqr
        s = str(x).split(".")
        l = int(s[0])
        r = int(s[1])
        lb = to_binaryfloat(l)
        rec(r)
        s1 = str(lb)
        s2 = str(wxx + '0' * (5 - len(wxx)))
        x = 0
        for u in s1:
            if u == '0':
                x += 1
            else:
                break
        wxx=''
        pqr=0
        return (s1[x:] + "." + s2)


    def convertToIeee(s):
        global wxx,pqr
        s1 = funcfordecimal(s)
        wxx=''
        pqr=0

        u = 0
        for i in s1[1:]:
            if i != ".":
                u += 1
            else:
                break

        w = ''
        w += s1[0]
        w += "."
        for i in s1[1:]:
            if i != ".":
                w += i

        exponent = to_binaryfloat(u)
    # print(exponent + w[2:7])
        return exponent + w[2:7]

    def to_float(s):  # vinayak function yahan banaio
        l = s[:3]
        r = s[3:]

        num = int(l,2)
        sum = 1
        for i in range(len(r)):
            if r[i] == "1":
                #  print(2** (-(i+1)))
                sum += 2 ** (-(i + 1))

        return (2 ** num) * sum





    def flag_str_to_int(s):
        u = 0
        for l in range(len(s)):

            u += int(s[l])#(2 * (len(s) - l - 1))

        return u


    def binary(n):
        s = ''
        b = 0
        while n >= 1:
            s += str(n % 2)
            n = n // 2
        return "0" * (8 - len(s)) + s[::-1]




    count = 0


    def apply(i):
        global pcNo, ErrorFlag, flag, addtoLabel, leng_instruction, x, halt_count
        k = i.split(" ")
        string = ""
        if list(k[0]) == []:
            k = k[1:]


        if k[0] == "var":
            try:
                assert len(k) == 2
                variables[k[1]] = leng_instruction - x
                leng_instruction += 1

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
                    assert k[0] == "mov" and k[2] in reg
                    dictreg[k[2]] = flag_str_to_int(flag)
                except AssertionError:
                    ErrorArray.append(f"ERROR: Illegal use of flag register at line {line_counter + 1}")
                    ErrorFlag += 1
                    return

        if k[0] == "mov" and k[2] not in register.keys():
            try:
                assert k[2][0] == "$"
                string += instruction["movi"] + register[k[1]] + binary(int(k[2][1:]))
            except AssertionError:
                ErrorArray.append(f"Error: Immediate value has incorrect syntax at line {line_counter + 1}")
                ErrorFlag += 1
                return

        if k[0] == "movf":
            try:
                if ("." in k[2][1:]):
                    string += "00010" + register[k[1]] + convertToIeee(k[2][1:])

                else:
                    assert int(k[2][1:]) <= 255
                    assert int(k[2][1:]) >= 0
                    string += instruction["movi"] + register[k[1]] + binary(int(k[2][1:]))
            except AssertionError:
                ErrorArray.append(f"ERROR: Illegal immediate value at line {line_counter + 1}")
                ErrorFlag += 1
                return

        if k[0] == "mov" and k[2] in register.keys():
            string += instruction["movr"] + "00000" + register[k[1]] + register[k[2]]

        if k[0] in ["add", "sub", "mul", "xor", "or", "and","addf","subf"]:
            try:
                assert len(k) >= 4
                if k[1] not in register.keys() or k[2] not in register.keys() or k[3] not in register.keys():
                    ErrorArray.append(f"ERROR: Invalid instruction syntax for {k[0]} at line  {line_counter + 1}")
                    addtoLabel = False
                    return
                if ("." in register[k[2]] or "." in register[k[3]]):
                    string += instruction[k[0]] + "00" + register[k[1]] + register[k[2]] + register[k[3]]

                else:
                    string += instruction[k[0]] + "00" + register[k[1]] + register[k[2]] + register[k[3]]

                if k[0] in ["add", "sub", "mul"]:
                    if k[0] == ("add" or "sub" or "mul") and dictreg[k[1]] == -1:
                        flag[-3] = 1
            except AssertionError:
                ErrorArray.append(f"ERROR: Insufficient Registers at line {line_counter + 1}")
                ErrorFlag += 1
                addtoLabel = False
                return

        if k[0] in ["ls", "rs"]:
            if k[1] not in reg.keys():
                ErrorArray.append(f"ERROR:Invalid instruction syntax at line {line_counter + 1}")
                ErrorFlag += 1
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
                if (k[2] in load_store):
                    string += instruction[k[0]] + register[k[1]] + binary(variables[k[2]])
                else:
                    load_store[k[2]] = leng_instruction - x
                    string += instruction[k[0]] + register[k[1]] + binary(variables[k[2]])
                    leng_instruction += 1
                pcNo += 1
            except AssertionError:
                ErrorArray.append(f"ERROR: Undeclared variable used at line {line_counter + 1}")
                ErrorFlag += 1
        if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] in label.keys():
            string += instruction[k[0]] + "000" + label[k[1]][0]

        if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] not in label.keys():
            ErrorArray.append(f"ERROR: Invalid memory address at line {line_counter + 1}")
            ErrorFlag += 1
            return
        if k[0] == "hlt":
            halt_count += 1
            try:
                assert halt_count == 1
                string += instruction[k[0]] + "00000000000"

            except AssertionError:
                ErrorArray.append(f"ERROR: Multiple halt instructions used")
                ErrorFlag += 1
        arr.append(string)


    def check_initial_label(i):
        global line_counter, addtoLabel, x, arr
        j = 0
        while (i[j] == " "):
            j += 1
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
                while (k[j] == ''):
                    j = j + 1
                # if (i[lb_len] == " ") and (i[lb_len + 1] != " "):
                if k[j] in instruction.keys() or k[j] == "mov":

                    d = []

                    d.append(binary(line_counter - x))

                    label[i[0:lb_len - 1]] = d
                    apply(str(i)[lb_len + j:])

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
        if k[0] == "var":
            x = x + 1

    for i in s:

        k = i.split(" ")
        if k[0] == "var":
            variables[k[1]] = 0

        if (ErrorFlag == 0):
            check_initial_label(i)
            line_counter += 1
        else:
            break
    halt_count = 0
    pcNo -= x
    line_counter = 0


    # checking if the immediate value is > 8bit

    def function(s):
        global line_counter, ErrorFlag
        for i in s:
            # check for illegal immediate value
            # immediate_check(i.split(" "))
            # will pass only the part of the string after a valid label
            if (ErrorFlag > 0):
                return
            j = 0
            while (i[j] == " "):
                j += 1
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
        while (i[j] == " "):
            j += 1
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
                while (k[j] == ''):
                    j = j + 1
                # if (i[lb_len] == " ") and (i[lb_len + 1] != " "):

                if k[j] in instruction.keys() or k[j] == "mov":
                    return label_len + j
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
            elif len(k) > 1:
                if k[1] in instruction.keys() or k[1] == "mov":
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
    variables = {}
    leng_instruction = leng_instruction_og
    load_store = {}
    if (ErrorFlag == 0):
        halt_count = 0
        ErrorArray = []
        ErrorFlag = 0
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

    if (len(arr) > 0 and ErrorFlag == 0):
        if arr[-1] == "0101000000000000":
            pass
        else:
            ErrorFlag += 1
            ErrorArray.append("ERROR: hlt not in given file")

    if ErrorFlag == 0 and len(ErrorArray) == 0:
        for i in range(x, len(arr)):
            print(arr[i])
    for i in ErrorArray:
        print(i)
    f.close()
    f = open('Myfile.txt', 'w')
    f.write("")
    f.close()
except:
        print(f"General syntax error at{line_counter+1}")
