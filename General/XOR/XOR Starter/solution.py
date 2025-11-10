from pwn import xor

label = b"label"
new = xor(label, 13)   # pwntools cho phép xor với số nguyên
print("crypto{" + new.decode() + "}")
