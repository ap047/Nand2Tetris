// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

(Set)
  @Screen
  D=A
  @0
  M=D
  @1
  M=-1

  //@8192
  //D=M
  @1
  M=D

  @2
  M=1
(Done)

(CHECK)
  @KBD
  D=M
  
  @Black
  D;JGT

  @2
  D=M
  @CHECK
  D;JGT

  @KBD
  D=M

  @White
  D;JEQ
    
  @CHECK
  0;JMP
(END)

(Black)
  @2
  M=0

  @0
  M=M+1
  @0
  A=M
  M=-1

  @1
  M=M-1
  D=M

  @CHECK
  D;JEQ

  @Black
  0;JMP
(End)

(White)
  @2
  M=1

  @0
  M=M-1
  @0
  A=M
  M=0

  @1
  M=M+1
  D=M

  @8192
  D=M-D
  @CHECK
  D;JEQ

  @White
  0;JEQ
(ENd)

