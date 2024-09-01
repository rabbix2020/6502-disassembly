from opcodes import *
from sys import argv
	
def dh(val):
	result = ('%X' % val)
	if len(result) < 2:	result = '0' + result
	return result

data = ''

if argv[1] != '':
	file = open(argv[1], "rb")
	data = file.read()

index = 0
while index < len(data):
	current_byte = dh(data[index])
	current_opcode_size = 1
	if current_byte in instruction_size.keys():
	   current_opcode_size = instruction_size[current_byte]
	   current_opcode = [current_byte] + list(map(dh, data[index+1:index+instruction_size[current_byte]]))
	   if current_opcode[0] in instruction_opcode:
	     match current_opcode_size:
	          case 1:	print(instruction_opcode[current_opcode[0]], end='')
	          case 2:
	                if not (instruction_opcode[current_opcode[0]][0:3] in branch_instructions):
	                  print(instruction_opcode[current_opcode[0]].format(oper='$' + current_opcode[1]), end='')
	                else:
	                    if int(current_opcode[1], 16) >= 128:
	                      print(instruction_opcode[current_opcode[0]].format(oper='$' + dh(index - (255 - 1 - int(current_opcode[1], 16)))), end='')
	                    else:	print(instruction_opcode[current_opcode[0]].format(oper='$' + dh(index + 2 + int(current_opcode[1], 16))), end='')
	          case 3:	print(instruction_opcode[current_opcode[0]].format(oper='$'+current_opcode[2]+current_opcode[1]), end='')
	   print("")
	else:	print(f".BYTE ${current_byte}")
	index += current_opcode_size
