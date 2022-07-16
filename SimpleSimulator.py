instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
                    "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
                    "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
                    "je": "01111", "hlt": "01010", "var": "00000"}

reg_codes = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110",
                "FLAGS": "111"}

reg_values = {"R0": 0, "R1":0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,
                "FLAGS": 0}

flag = {"V":0,"L":0,"G":0,"E":0}

def to_binary(num):
  s = str(bin(num))
  binary_num = s[2:]
  return binary_num

programmeCounter=0
halt = False
