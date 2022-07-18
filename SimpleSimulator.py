# instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
#                "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
#                "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
#                "je": "01111", "hlt": "01010", "var": "00000"}

import opcode


instruction = {"add": "00000", "sub": "00001", "ld": "00100", "st": "00101", "mul": "00110",
         "div": "00111", "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101",
         "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011",
         "movi":"00010","movr":"00011"
         }

# opcode = {"10000": "add", "10001": "sub", "10010": "movi", "10011": "movr", "10100": "ld", "10101": "ld",
#           "10110": "mul", "10111": "div", "11000": "rs", "11001": "ls", "11010": "xor", "11011": "or",
#           "11100": "and", "11101": "not", "11110": "cmp", "11111": "jmp", "01100": "jlt", "01101": "jgt",
#           "01111": "je", "01010": "hlt", "00000": "var"}

opcode = {'00000': 'add', '00001': 'sub', '00100': 'ld', '00101': 'st', '00110': 'mul', '00111': 'div', '01000': 'rs', '01001': 'ls', '01010': 'xor', '01011': 'or', '01100': 'and', '01101': 'not', '01110': 'cmp', '01111': 'jmp', '10000': 'jlt', '10001': 'jgt', '10010': 'je', '10011': 'hlt', '00010': 'movi','00011':'movr'}

reg_codes = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110",
             "FLAGS": "111"}

code_to_reg = {"000": "R0", "001": "R1", "010": "R2", "011": "R3", "100": "R4", "101": "R5", "110": "R6",
               "111": "FLAGS"}

reg_values = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,
              "FLAGS": 0}

flag = {"V": 0, "L": 0, "G": 0, "E": 0}

# type_A = ["10000", "10001", "10110", "11010", "11011", "11100"]
# type_B = ["10010", "11000", "11001"]
# type_C = ["10011", "10111", "11101", "11110"]
# type_D = ["10100", "10101"]
# type_E = ["11111", "01100", "01101", "01111"]
# type_F = ["01010"]
type_A = ['00000', '00001', '00110', '01010', '01011', '01100']
type_B = ['00010', '01000', '01001']
type_C = ['00011', '00111', '01101', '01110']
type_D = ['00100', '00101']
type_E = ['01111', '10000', '10001', '10010']
type_F = ['10011']

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
    reg_values['FLAGS'] = 12*'0'+str(flag["V"])+str(flag["L"])+str(flag["G"])+str(flag["E"])
    print(f"{to_binary(programmeCounter)} {to_16bit_binary(reg_values['R0'])} {to_16bit_binary(reg_values['R1'])} {to_16bit_binary(reg_values['R2'])} {to_16bit_binary(reg_values['R3'])} {to_16bit_binary(reg_values['R4'])} {to_16bit_binary(reg_values['R5'])} {to_16bit_binary(reg_values['R6'])} {(reg_values['FLAGS'])} ")

def to_binary(num):
    s = str(bin(num))
    binary_num = s[2:]
    if(len(binary_num)<8):
        binary_num=(8-len(binary_num))*'0'+binary_num
    return binary_num

def to_16bit_binary(num):
    s = str(bin(num))
    binary_num = s[2:]
    if(len(binary_num)<16):
        binary_num=(16-len(binary_num))*'0'+binary_num
    return binary_num

def to_int(s):
    return int(s, 2)


def arithmeticOperations(operation, regs1, regs2, regd):
    if operation == "add":
        if reg_values[regs1] + reg_values[regs2] > 255:
            flag["V"] = 1
            return
        reg_values[regd] = reg_values[regs1] + reg_values[regs2]
        values_print()
        return
    elif operation == "sub":
        if reg_values[regs1] - reg_values[regs2] < 0:
            flag["V"] = 1
        reg_values[regd] = reg_values[regs1] - reg_values[regs2]
        values_print()        
        return
    elif operation == "mul":
        if reg_values[regs1] * reg_values[regs2] > 255 or reg_values[regs1] * reg_values[regs2] < 0:
            flag["V"] = 1
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
    if operation == "movi":
        reg_values[regdes] = to_int(regval)
        values_print()
    if operation == "ls":
        reg_values[regdes] = reg_values[regdes] << to_int(regval)
        values_print()
        return
    if operation == "rs":
        reg_values[regdes] = reg_values[regdes] >> to_int(regval)
        values_print()
        return
def loadstore(operation,reg,mem):
    if operation=="ld":
        int_mem_add = to_int(mem)

        int_mem_add = int_mem_add-len(machine_code)
        load_value = memory_dump[int_mem_add]
        reg_values[code_to_reg[reg]] = to_int(load_value)
        values_print()
    if operation=="st":
        
        int_mem_add = to_int(mem)
        int_mem_add = int_mem_add-len(machine_code)
        memory_dump[int_mem_add] = to_16bit_binary(reg_values[code_to_reg[reg]])
        
        values_print()

while (not halt):
    machine_instruction = machine_code[programmeCounter]
    op = machine_instruction[0:5]
    
    operation = opcode[op]

    if (op in type_A):
        reg_source1 = machine_instruction[7:10]
        reg_source2 = machine_instruction[10:13]
        reg_dest = machine_instruction[13:16]
        arithmeticOperations(operation, code_to_reg[reg_source1], code_to_reg[reg_source2], code_to_reg[reg_dest])
    elif (op in type_B):
        reg_des = machine_instruction[5:8]
        imm_val = machine_instruction[8:16]
        if(op=="10010"):
          reg_values[code_to_reg[reg_des]]=to_int(imm_val)
          values_print()
        else:
          shiftoperation(operation, code_to_reg[reg_des], imm_val)
    elif (op in type_C):
        reg1 = machine_instruction[10:13]
        reg2 = machine_instruction[13:16]
        if(operation=="movr"):
          reg_values[code_to_reg[reg1]] = reg_values[code_to_reg[reg2]]
          values_print()
        elif(operation=="div"):
          reg_values[code_to_reg[reg1]] = reg_values[code_to_reg[reg1]]/reg_values[code_to_reg[reg2]]
          reg_values[code_to_reg[reg2]] = reg_values[code_to_reg[reg1]]%reg_values[code_to_reg[reg2]]
          values_print()
        elif(operation=="not"):
          reg_values[code_to_reg[reg2]] = ~reg_values[code_to_reg[reg1]]
          values_print()
        elif(operation=="cmp"):
          flag["V"]=0
          flag["L"]=0
          flag["E"]=0
          flag["G"]=0
          if(reg_values[code_to_reg[reg1]]==reg_values[code_to_reg[reg2]]):
            flag["E"] = 1
          elif(reg_values[code_to_reg[reg1]]>reg_values[code_to_reg[reg2]]):
            flag["G"] = 1
          elif(reg_values[code_to_reg[reg1]]<reg_values[code_to_reg[reg2]]):
            flag["L"] = 1
          values_print()
    elif (op in type_D):
        reg1 = machine_instruction[5:8]
        memory_address = machine_instruction[8:16]
        loadstore(operation,reg1,memory_address)


    elif (op in type_E):
        memory_address = machine_instruction[8:16]
        if operation=="jmp":
            values_print()
            programmeCounter = to_int(memory_address)
            continue
        elif operation=="jlt":
            if flag["L"]==1:
                values_print()
                programmeCounter = to_int(memory_address)
                continue
            else:
                values_print()
        elif operation=="jgt":
            if flag["G"]==1:
                values_print()
                programmeCounter = to_int(memory_address)
                continue
            else:
                values_print()
        elif operation=="je":
            if flag["E"]==1:
                values_print()
                programmeCounter = to_int(memory_address)
                continue
            else:
               values_print()

    elif (op in type_F):
        halt = True
    
    programmeCounter+=1


for i in range(len(machine_code)):
    print(machine_code[i])
   

for i in range(dump_len):
    print(memory_dump[i])