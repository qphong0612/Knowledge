# PWN methodology - LINUX

## Basic binary security checks and some bypass:
- **ALSR** - Partial Overwrite/ Info Disclosure/ Brute Force 
- **DEP** - mprotect()/ ret2libc/ ROP/ Egghunter
- **RELRO** - GOT overwrite/ .fini_array overwrite/ .dtors overwrite
- **PIE** - Address leak/ NOP slide 
- **Stack canaries** - Brute force/ Heap overflows/ Arbitrary Write
- **Architecture** - OS 32/64 ?
- **Library Linking** - Dynamically/ Statically linked
- **Debug infor** - Stripped/ not Stripped

Check ASLR is on 
```
cat /proc/sys/kernel/randomize_va_space
```

## Run the binary with:
```
ltrace ./$bin_name
strace ./$bin_name
gdb -q ./$bin_name
```

## Decompile & disassembly of the file 
```
IIDA,Ghidra, Hopper
```
## Check function address 

      objdump -D ./$bin_name -j .text -M intel
      objdump -TR ./$bin_name
      readelf -S ./$bin_name

## GDB and GEF
### Starting gdb
```
gbd program [core|pid]
gdb gdb-option [--args program agrs]
gdb -p pid 
```

At startup, gdb reads following the init files and execute commands: `/etc/gdb/gdbinit` and `~/.gdbinit` plus `./gdbinit` 
