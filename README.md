# pyhackassembler

This repo contains my implementation of the final project from Nand2Tetris (part 1), which converts Hack assembly code into binary machine code.

Takes a Hack assembly (`.asm`) file containing e.g.

```
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/add/Add.asm

// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
```

and produces the equivalent binary code as a `.hack` file:

```
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000

```

## Example usage

To run the code:

```py
python3 ./assembler/assembler.py ./add/Add.asm
```

