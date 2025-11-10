from pwn import xor

hex_data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
bytes_str = bytes.fromhex(hex_data)
res = ""
flag = ""
for num in range(256):
    res = xor(num, bytes_str)
    if b'crypto' in res:
        break
flag = res.decode()
print (flag)