/* -- test.s */
.global main /* 'main' is our entry point and must be global */

main: /* This is main */
    mvn r0, #13
    mvn r1, #13
    and r0, r1
    mvn r0, r0
    bx lr /* Return from main */
