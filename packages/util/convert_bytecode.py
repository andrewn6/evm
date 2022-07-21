import sys
import os

def convert():
  if len(sys.argv) != 3:
    print("**Usage: python3 convert_bytecode.py [example].evm output.bytecode**")
    sys.exit()

  filename_input = sys.argv[1]
  filename_output = sys.argv[2]

  f = open(filename_input, 'r')
  code = f.read()
  f.close()

  # Replace with hex code
  code = code.replace('\n', "").decode('hex')

  f = open(filename_output, "wb")
  f.write("evm")
  f.write(code)
  f.close()

if __name__ == "__main__":
  convert()
