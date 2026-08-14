.export _main

.include "rp6502.inc"

.segment "RODATA"

message:
    .byte "Hello, world!", $0D, $0A, 0

.segment "CODE"

; Entry point. The C runtime has already set the stack pointer and cleared
; decimal mode, and it halts the 6502 with the status we return.
_main:

; Print "Hello, world!" message
    ldx #0
@loop:
    lda message,x
    beq @done           ; If zero, we're done
@wait:
    bit RIA_READY       ; Waiting on UART tx ready
    bpl @wait
    sta RIA_TX          ; Transmit the byte
    inx
    bne @loop           ; Continue loop
@done:

; Exit status
    lda #0
    ldx #0
    rts
