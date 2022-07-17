instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
                    "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
                    "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
                    "je": "01111", "hlt": "01010", "var": "00000"}

opcode = {"10000":"add","10001":"sub", "10010":"movi", "10011":"movr",  "10100":"ld",  "10101":"ld",
                     "10110":"mul",  "10111":"div",  "11000":"rs",  "11001":"ls",  "11010":"xor", "11011":"or",
                     "11100":"and",  "11101":"not",  "11110":"cmp", "11111":"jmp", "01100":"jlt", "01101":"jgt",
                     "01111":"je", "01010":"hlt", "00000":"var"}

reg_codes = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110",
                "FLAGS": "111"}

code_to_reg = { "000":"R0",  "001":"R1",  "010":"R2",  "011":"R3",  "100":"R4",  "101":"R5", "110":"R6",
               "111":"FLAGS"}

reg_values = {"R0": 0, "R1":0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,
                "FLAGS": 0}

flag = {"V":0,"L":0,"G":0,"E":0}

type_A = ["10000","10001","10110","11010","11011","11100"]
type_B = ["10010","11000","11001"]
type_C = ["10011","10111","11101","11110"]
type_D = ["10100","10101"]
type_E = ["11111","01100","01101","01111"]
type_F = ["01010"]



programmeCounter=0
halt = False

machine_code = []
while(True):
  try:
    s = input()
    machine_code.append(s)
  except EOFError:
    break

dump_len = 256-len(machine_code)
og_dump = '0'*16
memory_dump = []
for i in range(dump_len):
  memory_dump.append(og_dump)

def to_binary(num):
  s = str(bin(num))
  binary_num = s[2:]
  return binary_num

while(not halt):
  machine_instruction = machine_code[programmeCounter]
  op = machine_code[0:5]
  operation = opcode[op]

  if(op in type_A):
    reg_dest = machine_code[7:10]
    reg_source1 = machine_code[10:13]
    reg_source2 = machine_code[13:16]
     
  elif(op in type_B):
    reg_des = machine_code[5:8]
    imm_val = machine_code[8:16]
  elif(op in type_C):
    reg1 = machine_code[10:13]
    reg = machine_code[13:16]
  elif(op in type_D):
    reg1 = machine_code[5:8]
    memory_address = machine_code[8:16]

  elif(op in type_E):
     memory_address = machine_code[8:16]
  elif(op in type_F):
    halt = True