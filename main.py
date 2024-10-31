import re

def assemblyfuck_to_nasm(af_code):
    nasm_code = []
    memory_size = 30000  

    # Define memory setup
    nasm_code.append("section .bss")
    nasm_code.append(f"mem resb {memory_size}")  
    nasm_code.append("")
    
    nasm_code.append("section .text")
    nasm_code.append("global _start")
    nasm_code.append("_start:")

    lines = af_code.splitlines()

    for line in lines:
        line = line.strip()
        
        # ADD <VALUE>, <TARGET>
        if line.startswith("ADD"):
            match = re.match(r'ADD\s+(\d+)\s*,\s*(\d+)', line)
            if match:
                value, target = match.groups()
                nasm_code.append(f"    add byte [mem + {target}], {value}")

        # SUB <VALUE>, <TARGET>
        elif line.startswith("SUB"):
            match = re.match(r'SUB\s+(\d+)\s*,\s*(\d+)', line)
            if match:
                value, target = match.groups()
                nasm_code.append(f"    sub byte [mem + {target}], {value}")
        
        # MOV <VALUE>, <TARGET>
        elif line.startswith("MOV"):
            match = re.match(r'MOV\s+(\d+)\s*,\s*(\d+)', line)
            if match:
                value, target = match.groups()
                nasm_code.append(f"    mov byte [mem + {target}], {value}")
        
        # CMP <CELL NUMBER>, <NUMBER>
        elif line.startswith("CMP"):
            match = re.match(r'CMP\s+(\d+)\s*,\s*(\d+)', line)
            if match:
                cell, number = match.groups()
                nasm_code.append(f"    cmp byte [mem + {cell}], {number}")

        # JE <TAG>
        elif line.startswith("JE"):
            match = re.match(r'JE\s+(\w+)', line)
            if match:
                tag = match.groups()[0]
                nasm_code.append(f"    je {tag}")

        # JNE <TAG>
        elif line.startswith("JNE"):
            match = re.match(r'JNE\s+(\w+)', line)
            if match:
                tag = match.groups()[0]
                nasm_code.append(f"    jne {tag}")

        # Tags / labels
        elif re.match(r'\w+:', line):
            nasm_code.append(f"{line}")
    
    # exit using linux syscall doesnt work on windows!
    nasm_code.append("    mov eax, 60")  
    nasm_code.append("    xor edi, edi")  
    nasm_code.append("    syscall")

    return "\n".join(nasm_code)


assemblyfuck_code = """
MOV 72, 0
MOV 101, 1
MOV 108, 2
MOV 108, 3
MOV 111, 4
MOV 32, 5
MOV 87, 6
MOV 111, 7
MOV 114, 8
MOV 108, 9
MOV 100, 10
"""

nasm_output = assemblyfuck_to_nasm(assemblyfuck_code)
print(nasm_output)
