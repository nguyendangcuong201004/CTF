from pwn import xor

cipher_hex = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
cipher_bytes = bytes.fromhex(cipher_hex)

# cipher_text = Plaintext ^ key
# plaintext = ciphertext ^ key
# key = plaintext ^ ciphertext

plain_part = b"crypto{"

print (cipher_bytes)
key_part = xor (cipher_bytes[:7], plain_part)
print ("Key part:", key_part)

key_guess = b'myXORkey'
flag = xor(cipher_bytes, key_guess)
print ("flag: ", flag.decode())