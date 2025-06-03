# hw4
```
user@DESKTOP-G45H2SD:/mnt/d/Users/Yu^2/Desktop/金大資工/大四下/系統程式/sp/_sp/hw4/04-maxofthree$ gcc -std=c99 mul3.c mul3.s
/usr/bin/ld: warning: /tmp/ccnqq8xv.o: missing .note.GNU-stack section implies executable stack
/usr/bin/ld: NOTE: This behaviour is deprecated and will be removed in a future version of the linker
user@DESKTOP-G45H2SD:/mnt/d/Users/Yu^2/Desktop/金大資工/大四下/系統程式/sp/_sp/hw4/04-maxofthree$ ./a.out
mul3(3,2,5)=30
```

mul3.s標註 15~18row
mult3接收三個參數（分別透過 %rdi, %rsi, %rdx 傳遞），回傳它們的乘積。結果儲存在 %rax(回傳值暫存器)