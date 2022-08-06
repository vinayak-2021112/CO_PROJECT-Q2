import matplotlib.pyplot as p
instruction = {"add": "10000","addf": "00000", "sub": "10001","subf": "0001", "movi": "10010","movf": "00010", "movr": "10011", "ld": "10100", "st": "10101",
               "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
               "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
               "je": "01111", "hlt": "01010", "var": "00000"}

opcode = {"10000": "add","00000": "addf", "10001": "sub","00001": "subf", "10010": "movi","00010": "movf","10011": "movr", "10100": "ld", "10101": "st",
          "10110": "mul", "10111": "div", "11000": "rs", "11001": "ls", "11010": "xor", "11011": "or",
          "11100": "and", "11101": "not", "11110": "cmp", "11111": "jmp", "01100": "jlt", "01101": "jgt",
          "01111": "je", "01010": "hlt"}

reg_codes = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110",
             "FLAGS": "111"}

code_to_reg = {"000": "R0", "001": "R1", "010": "R2", "011": "R3", "100": "R4", "101": "R5", "110": "R6",
               "111": "FLAGS"}

reg_values = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,
              "FLAGS": 0}

flag = {"V": 0, "L": 0, "G": 0, "E": 0}
cycles = {}

type_A = ["00000","00001","10000", "10001", "10110", "11010", "11011", "11100"]
type_B = ["00010","10010", "11000", "11001"]
type_C = ["10011", "10111", "11101", "11110"]
type_D = ["10100", "10101"]
type_E = ["11111", "01100", "01101", "01111"]
type_F = ["01010"]
programmeCounter = 0
halt = False

machine_code = []
while (True):
    try:
        s = input()
        machine_code.append(s)
    except EOFError:
        break

dump_len = 256 - len(machine_code)
og_dump = '0' * 16
memory_dump = []
for i in range(dump_len):
    memory_dump.append(og_dump)


def values_print():
    reg_values['FLAGS'] = 12 * '0' + str(flag["V"]) + str(flag["L"]) + str(flag["G"]) + str(flag["E"])
    print(
        f"{to_binary(programmeCounter)} {to_16bit_binary(reg_values['R0'])} {to_16bit_binary(reg_values['R1'])} {to_16bit_binary(reg_values['R2'])} {to_16bit_binary(reg_values['R3'])} {to_16bit_binary(reg_values['R4'])} {to_16bit_binary(reg_values['R5'])} {to_16bit_binary(reg_values['R6'])} {(reg_values['FLAGS'])}")



def to_binary(num):

    s = str(bin(num))
    binary_num = s[2:]
    if (len(binary_num) < 8):
        binary_num = (8 - len(binary_num)) * '0' + binary_num
    return binary_num


def to_16bit_binary(num):
    if isinstance(num, float):
        return 8 * '0' + convertToIeee(num)
    s = str(bin(num))
    binary_num = s[2:]
    if (len(binary_num) < 16):
        binary_num = (16 - len(binary_num)) * '0' + binary_num
    if (len(binary_num) > 16):
        ind = len(binary_num) - 16
        binary_num = binary_num[ind:]
    return binary_num


def to_float(s): 
    l = s[:3]
    r = s[3:]

    num = to_int(l)
    sum=1
    for i in range(len(r)):
        if r[i]=="1":
            sum += 2** (-(i+1))

    return (2**num)*sum



def to_int(s):
    return int(s, 2)


def set_flag_zero(flag):
    for i in flag:
        flag[i] = 0


def to_binaryf(num):
    s = str(bin(num))
    binary_num = s[2:]
    if (len(binary_num) < 8):
        binary_num = (3 - len(binary_num)) * '0' + binary_num
    return binary_num

def to_16binaryforfloat(s):
    return 8*'0'+s


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
    return exponent + w[2:7]


def arithmeticOperations(operation, regs1, regs2, regd):
    if operation == "addf":
        if reg_values[regs1] + reg_values[regs2] > 252:
            flag["V"] = 1
            
            reg_values[regd] = 252
            values_print()
            return
        reg_values[regd] = reg_values[regs1] + reg_values[regs2]

        values_print()
        return
    if operation == "add":

        if reg_values[regs1] + reg_values[regs2] > 65535:
            flag["V"] = 1
            large = 2 ** 16
            sum_over = reg_values[regs1] + reg_values[regs2]
            reg_values[regd] = sum_over % large
            values_print()
            return
        reg_values[regd] = reg_values[regs1] + reg_values[regs2]

        values_print()
        return
    elif operation == "subf":
        if reg_values[regs1] - reg_values[regs2] < 0:
            flag["V"] = 1
            reg_values[regd] = 0
            values_print()
            return
        reg_values[regd] = reg_values[regs1] - reg_values[regs2]
        values_print()
        return

    elif operation == "sub":
        if reg_values[regs1] - reg_values[regs2] < 0:
            flag["V"] = 1
            reg_values[regd] = 0
            values_print()
            return
        reg_values[regd] = reg_values[regs1] - reg_values[regs2]
        values_print()
        return
    elif operation == "mul":
        if reg_values[regs1] * reg_values[regs2] > 65535 or reg_values[regs1] * reg_values[regs2] < 0:
            flag["V"] = 1
            large = 2 ** 16
            mul_over = reg_values[regs1] * reg_values[regs2]
            reg_values[regd] = mul_over % large
            values_print()
            return
        reg_values[regd] = reg_values[regs1] * reg_values[regs2]
        values_print()
        return
    elif operation == "xor":
        reg_values[regd] = reg_values[regs1] ^ reg_values[regs2]
        values_print()
        return
    elif operation == "or":
        reg_values[regd] = reg_values[regs1] | reg_values[regs2]
        values_print()
        return
    elif operation == "and":
        reg_values[regd] = reg_values[regs1] & reg_values[regs2]
        values_print()
        return


def shiftoperation(operation, regdes, regval):
    if operation == "movf":
        reg_values[regdes] = to_float(regval)
        values_print()
        return
    if operation == "movi":
        reg_values[regdes] = to_int(regval)
        values_print()
        return
    if operation == "ls":
        reg_values[regdes] = reg_values[regdes] << to_int(regval)
        values_print()
        return
    if operation == "rs":
        reg_values[regdes] = reg_values[regdes] >> to_int(regval)
        values_print()
        return


def loadstore(operation, reg, mem):

    if operation == "ld":
        int_mem_add = to_int(mem)
        int_mem_add = int_mem_add - len(machine_code)
        load_value = memory_dump[int_mem_add]
        reg_values[code_to_reg[reg]] = to_int(load_value)
        values_print()
    if operation == "st":

        int_mem_add = to_int(mem)
        int_mem_add = int_mem_add - len(machine_code)
        memory_dump[int_mem_add] = to_16bit_binary(reg_values[code_to_reg[reg]])

        values_print()

def update_cycles(cycles, programmecounter):
    n = len(cycles)

    if (n == 0):
        cycles[0] = programmecounter
        return

    cycles[n] = programmecounter
while (not halt):
    machine_instruction = machine_code[programmeCounter]
    op = machine_instruction[0:5]

    operation = opcode[op]

    if (op in type_A):
        set_flag_zero(flag)
        reg_source1 = machine_instruction[7:10]
        reg_source2 = machine_instruction[10:13]
        reg_dest = machine_instruction[13:16]
        arithmeticOperations(operation, code_to_reg[reg_source1], code_to_reg[reg_source2], code_to_reg[reg_dest])
    elif (op in type_B):
        set_flag_zero(flag)
        reg_des = machine_instruction[5:8]
        imm_val = machine_instruction[8:16]
        if (op == "10010"):
            reg_values[code_to_reg[reg_des]] = to_int(imm_val)
            values_print()
        else:
            shiftoperation(operation, code_to_reg[reg_des], imm_val)
    elif (op in type_C):

        reg1 = machine_instruction[10:13]
        reg2 = machine_instruction[13:16]
        if (operation == "movr"):
            if (code_to_reg[reg1] == "FLAGS"):
                flag_val = to_int(str(flag["V"]) + str(flag["L"]) + str(flag["G"]) + str(flag["E"]))

                reg_values[code_to_reg[reg2]] = flag_val
            
            else:
                reg_values[code_to_reg[reg2]] = reg_values[code_to_reg[reg1]]
            set_flag_zero(flag)
            values_print()
        elif (operation == "div"):
            set_flag_zero(flag)
            x = reg_values[code_to_reg[reg1]]
            y = reg_values[code_to_reg[reg2]]
            reg_values["R0"] = x // y
            reg_values["R1"] = x % y
            values_print()
        elif (operation == "not"):
            set_flag_zero(flag)
            a = to_16bit_binary(reg_values[code_to_reg[reg1]])
            final = ''
            for i in range(16):
                if(a[i]=='0'):
                    final=final+'1'
                else:
                    final = final+'0'
            final_val = to_int(final)
            reg_values[code_to_reg[reg2]] = final_val
            values_print()
        elif (operation == "cmp"):
            set_flag_zero(flag)
            if (reg_values[code_to_reg[reg1]] == reg_values[code_to_reg[reg2]]):
                flag["E"] = 1
            elif (reg_values[code_to_reg[reg1]] > reg_values[code_to_reg[reg2]]):
                flag["G"] = 1
            elif (reg_values[code_to_reg[reg1]] < reg_values[code_to_reg[reg2]]):
                flag["L"] = 1
            values_print()
    elif (op in type_D):
        set_flag_zero(flag)
        reg1 = machine_instruction[5:8]
        memory_address = machine_instruction[8:16]
        loadstore(operation, reg1, memory_address)
      


    elif (op in type_E):

        
        if operation == "jmp":
            set_flag_zero(flag)
            memory_address = machine_instruction[8:16]
            values_print()
            programmeCounter = to_int(memory_address)
            continue
        elif operation == "jlt":
            if flag["L"] == 1:
                set_flag_zero(flag)
                values_print()
                memory_address = machine_instruction[8:16]
                programmeCounter = to_int(memory_address)
                continue
            else:
                set_flag_zero(flag)
                values_print()
        elif operation == "jgt":
            if flag["G"] == 1:
                set_flag_zero(flag)
                values_print()
                memory_address = machine_instruction[8:16]
                programmeCounter = to_int(memory_address)
                continue
            else:
                set_flag_zero(flag)
                values_print()
        elif operation == "je":
            if flag["E"] == 1:
                set_flag_zero(flag)
                values_print()
                memory_address = machine_instruction[8:16]
                programmeCounter = to_int(memory_address)
                continue
            else:
                set_flag_zero(flag)
                values_print()

    elif (op in type_F):
        set_flag_zero(flag)
        halt = True
        values_print()
    update_cycles(cycles, programmeCounter)
    programmeCounter += 1

for i in range(len(machine_code)):
    print(machine_code[i])

for i in range(dump_len):
    print(memory_dump[i])


cycle_count = list(cycles.keys())
mem_address = list(cycles.values())

# p.scatter(mem_address,cycle_count)
# p.ylabel("Cycle Counter")
# p.xlabel("Memory addres")
# p.show()
