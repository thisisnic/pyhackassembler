import sys
import os
import re

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

def process_contents(contents):
    instructions = []
    symbol_table = [
        {"number": 0, "value": "SP"}, {"number": 1, "value": "LCL"}, 
        {"number": 2, "value": "ARG"}, {"number": 3, "value": "THIS"}, 
        {"number": 4, "value": "THAT"},
        {"number": 16384, "value": "SCREEN"},{"number": 24576, "value": "KBD"}
        ]
    var_ref = 16

    lines = contents.split("\n")

    i = 0
    # first pass to set up symbol table
    for line in lines:
        
        line = line.replace(" ", "")
        
        if is_comment(line) or is_empty(line):
                    continue
        elif is_symbol_location(line):
                symb = line.replace("(", "").replace(")", "")
                match = [x["number"] for x in symbol_table if x["value"] == symb]
                if not match:
                    symbol_table.append({"number": i, "value": symb})
        else:
            i += 1
                    
    # second pass to work out instructions

    for line in lines:
        line = line.replace(" ", "")
        
        if is_comment(line) or is_empty(line) or is_symbol_location(line):
            continue

        elif is_a_instruction(line):
            # work out if it's a ref or a value
            ref = get_reference(line)
            if(ref["symbol"]):
                match = [x["number"] for x in symbol_table if x["value"] == ref["value"]]
                if match:
                    instructions.append(int_to_bin(match[0]))
                else:
                    # if it's just a variable
                    symbol_table.append({"number": var_ref, "value": ref["value"]})
                    instructions.append(int_to_bin(var_ref))
                    var_ref += 1
            else:
                instructions.append(int_to_bin(int(ref["value"])))
        else:
            instructions.append(process_type_c(line))            
                            
    return instructions


def is_comment(line):
    return line.startswith("//")

def is_empty(line):
    return line == ""

def is_symbol_location(line):
    return line.startswith("(")

def is_a_instruction(line):
    return line.startswith("@")


def int_to_bin(num):
    return format(num, '016b')

def process_type_c(line):

    line = line.split("//")[0]

    binary_string = '111'
    dest = ""
    jump = ""
    if "=" in line:
        line_components = line.split("=")
        dest = line_components[0]
        line = line_components[1]

    if ";" in line:
        line_components = line.split(";")
        jump = line_components[1]
        line = line_components[0]

    comp = line


    return binary_string + translate_comp(comp) + translate_dest(dest) + translate_jump(jump)

def get_reference(line):
    ref = {}
    # remove the @
    ref_val = line[1:]
    # remove any R references
    ref_val = re.sub(r"^R{1}(?=[0-9]{1,2})", "", ref_val)
    
    ref["symbol"] = not ref_val.isdigit()
    ref["value"] = ref_val

    return ref


def write_to_file(processed_contents, output_file_path):
    try:
        with open(output_file_path, 'w') as file:
            for instruction in processed_contents:
                file.write(f"{instruction}\n")
        print("Processed contents written to", output_file_path)
    except Exception as e:
        print("An error occurred while writing to the file:", e)

       
def translate_comp(comp):
    match comp:
        case "0":
            return "0101010"
        case "1":
            return "0111111"
        case "-1":
            return "0111010"
        case "D":
            return "0001100"
        case "A":
            return "0110000"
        case "!D":
            return "0001101"
        case "!A":
            return "0110011"
        case "D+1":
            return "0011111"
        case "A+1":
            return "0110111"
        case "D-1":
            return "0001110"
        case "A-1":
            return "0110010"
        case "D+A":
            return "0000010"
        case "D-A":
            return "0010011"
        case "A-D":
            return "0000111"
        case "D&A":
            return "0000000"
        case "D|A":
            return "0010101"
        case "M":
            return "1110000"
        case "!M":
            return "1110001"
        case "-M":
            return "1110011"
        case "M+1":
            return "1110111"
        case "M-1":
            return "1110010"
        case "D+M":
            return "1000010"
        case "D-M":
            return "1010011"
        case "M-D":
            return "1000111"
        case "D&M":
            return "1000000"
        case "D|M":
            return "1010101"

def translate_jump(jump):
    match jump:
        case "":
            return "000"
        case "JGT":
            return "001"
        case "JEQ":
            return "010"
        case "JGE":
            return "011"
        case "JLT":
            return "100"
        case "JNE":
            return "101"
        case "JLE":
            return "110"
        case "JMP":
            return "111"

def translate_dest(dest):
    match dest:
        case "":
            return "000"
        case "M":
            return "001"
        case "D":
            return "010"
        case "MD":
            return "011"
        case "A":
            return "100"
        case "AM":
            return "101"
        case "AD":
            return "110"
        case "AMD":
            return "111"


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]

    # Extracting the filename without extension
    file_name, _ = os.path.splitext(os.path.basename(input_file_path))
    
    # Generating the output file path with the ".hack" suffix
    output_file_path = f"{file_name}.hack"

    file_contents = read_file(input_file_path)
    if file_contents:
        processed_contents = process_contents(file_contents)
        write_to_file(processed_contents, output_file_path)

if __name__ == "__main__":
    main()
