from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

r = remote('socket.cryptohack.org', 13377)

# Cau nay em co tham khao writeup tren internet va AI

def decode_data(encoding_type, encoded_data):
    if encoding_type == "base64":
        return base64.b64decode(encoded_data).decode()
    elif encoding_type == "hex":
        return bytes.fromhex(encoded_data).decode()
    elif encoding_type == "rot13":
        return codecs.decode(encoded_data, 'rot_13')
    elif encoding_type == "bigint":
        # encoded_data có dạng: '0x...'
        big_int = int(encoded_data, 16)
        return long_to_bytes(big_int).decode()
    elif encoding_type == "utf-8":
        # encoded_data là list các số: [65, 66, 67]
        return ''.join(chr(b) for b in encoded_data)
    else:
        return None

# Xử lý 100 levels
for level in range(100):
    # Nhận dữ liệu từ server
    data = r.recvline().decode().strip()
    challenge = json.loads(data)
    
    print(f"Level {level + 1}: {challenge['type']}")
    
    # Decode dữ liệu
    decoded = decode_data(challenge['type'], challenge['encoded'])
    
    # Gửi kết quả
    response = {"decoded": decoded}
    r.sendline(json.dumps(response).encode())

# Nhận flag
flag_data = r.recvline().decode().strip()
print(flag_data)
r.close()