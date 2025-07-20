.export _init, _exit
.export __STARTUP__ : absolute = 1

.include "rp6502.inc"

.segment "CODE"

; Entry point
_init:
    ; 6502 doesn't reset these
    ldx #$FF
    txs
    cld

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

; Halts the 6502 by pulling RESB low
_exit:
    lda #RIA_OP_EXIT
    sta RIA_OP

.segment "RODATA"

message:
    .byte "Hello, world!", $0D, $0A, 0
