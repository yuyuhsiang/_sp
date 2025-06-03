# hw5
執行a.cpp
```
gcc a.c -o a
```
產生組合語言.s檔
```
gcc -S a.c
```
產生目的檔.o檔
```
gcc -c a.c
```
將該目的檔反組譯
```
objdump -d a.o
```
```
a.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <power2>:
   0:   f3 0f 1e fa             endbr64
   4:   55                      push   %rbp
   5:   48 89 e5                mov    %rsp,%rbp
   8:   89 7d ec                mov    %edi,-0x14(%rbp)
   b:   c7 45 f8 01 00 00 00    movl   $0x1,-0x8(%rbp)
  12:   c7 45 fc 01 00 00 00    movl   $0x1,-0x4(%rbp)
  19:   eb 07                   jmp    22 <power2+0x22>
  1b:   d1 65 f8                shll   $1,-0x8(%rbp)
  1e:   83 45 fc 01             addl   $0x1,-0x4(%rbp)
  22:   8b 45 fc                mov    -0x4(%rbp),%eax
  25:   3b 45 ec                cmp    -0x14(%rbp),%eax
  28:   7e f1                   jle    1b <power2+0x1b>
  2a:   8b 45 f8                mov    -0x8(%rbp),%eax
  2d:   5d                      pop    %rbp
  2e:   c3                      ret

000000000000002f <main>:
  2f:   f3 0f 1e fa             endbr64
  33:   55                      push   %rbp
  34:   48 89 e5                mov    %rsp,%rbp
  37:   bf 03 00 00 00          mov    $0x3,%edi
  3c:   e8 00 00 00 00          call   41 <main+0x12>
  41:   89 c6                   mov    %eax,%esi
  43:   48 8d 05 00 00 00 00    lea    0x0(%rip),%rax        # 4a <main+0x1b>
  4a:   48 89 c7                mov    %rax,%rdi
  4d:   b8 00 00 00 00          mov    $0x0,%eax
  52:   e8 00 00 00 00          call   57 <main+0x28>
  57:   b8 00 00 00 00          mov    $0x0,%eax
  5c:   5d                      pop    %rbp
  5d:   c3                      ret
```
印出該目的檔的表頭
```
objdump -h a.o
```
```
a.o:     file format elf64-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .text         0000005e  0000000000000000  0000000000000000  00000040  2**0
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE
  1 .data         00000000  0000000000000000  0000000000000000  0000009e  2**0
                  CONTENTS, ALLOC, LOAD, DATA
  2 .bss          00000000  0000000000000000  0000000000000000  0000009e  2**0
                  ALLOC
  3 .rodata       0000000e  0000000000000000  0000000000000000  0000009e  2**0
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  4 .comment      0000002c  0000000000000000  0000000000000000  000000ac  2**0
                  CONTENTS, READONLY
  5 .note.GNU-stack 00000000  0000000000000000  0000000000000000  000000d8  2**0
                  CONTENTS, READONLY
  6 .note.gnu.property 00000020  0000000000000000  0000000000000000  000000d8  2**3
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  7 .eh_frame     00000058  0000000000000000  0000000000000000  000000f8  2**3
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA
```