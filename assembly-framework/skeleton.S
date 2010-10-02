segment .data
segment .bss
segment .text
	global asm_main
asm_main:
enter 0,0
pusha
;start inserting code here



;end of code
popa
mov           eax,0
leave
ret

