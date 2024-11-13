// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.
// Multiplies R0 with R1
@2
M=0

@0
D=M
@DONE
D;JEQ

@1 // irefers tosome mem. location.
D=M
@DONE
D;JEQ

(LOOP)
    @0
    M=M-1 
    
    @1
    D=M
    @2
    M=D+M
    
    @0
    D=M
    @END
    D;JEQ

    @LOOP
    0;JMP

(END)

@DONE
@END
0;JMP // Infiniteloop