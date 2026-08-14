.globl main

.include "rp6502.inc"

.section .rodata,"a",@progbits

message:
    .asciz "Hello, world!\r\n"

.section .text,"ax",@progbits

; Entry point. The C runtime has already set the stack pointer and cleared
; decimal mode, and it halts the 6502 with the status we return.
main:

; Print "Hello, world!" message
    ldx #0
1:
    lda message,x
    beq 2f              ; If zero, we're done
3:
    bit RIA_READY       ; Waiting on UART tx ready
    bpl 3b
    sta RIA_TX          ; Transmit the byte
    inx
    bne 1b              ; Continue loop
2:

; Exit status
    lda #0
    ldx #0
    rts
