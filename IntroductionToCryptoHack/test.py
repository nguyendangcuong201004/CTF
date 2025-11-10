from fastecdsa.curve import Curve
from fastecdsa.point import Point
from Crypto.Cipher import AES
import hashlib
import math

# Định nghĩa curve (giống đề bài)
p = 81663996540811672901764249733343363790991183353803305739092974199965546219729
a = 1
b = 7
Gx = 14023374736200111073976017545954000619736741127496973904317708826835398305431
Gy = 23173384182409394365116200040829680541979866476670477159886520495530923549144
Px = 63698676086974127123544556591037049117285370657094973402459055228534678256540
Py = 50054613692038253008132268195064761802561717815733137655094406841864102707369

ciphertext_hex = '701d3fed9cf7f5182f2e924ed9f9d23a9a0bf21ac6bf877bb53f6ceb27ae86551df3f27d8820c4bd2552f4953406ba18'
iv_hex = '8d79f0db12f8d54f2fd70d067340124f'

ciphertext = bytes.fromhex(ciphertext_hex)
iv = bytes.fromhex(iv_hex)

# Tạo curve
curve = Curve("custom", p, a, b, Gx, Gy, 1, 1)  # order tạm 1, vì không dùng
G = Point(Gx, Gy, curve)
P = Point(Px, Py, curve)

# Baby-step giant-step tự implement
def bsgs_ecdlp(P, G, max_bits=64):
    m = int(math.isqrt(2**max_bits)) + 1
    # Baby steps
    baby = {}
    current = G * 0  # điểm vô cực?
    for j in range(m):
        baby[current] = j
        current = current + G
    # Giant step
    factor = G * (-m)
    current = P
    for i in range(m):
        if current in baby:
            j = baby[current]
            return i * m + j
        current = current + factor
    return None

x = bsgs_ecdlp(P, G)
print("x =", x)

# Giải mã
sha1 = hashlib.sha1()
sha1.update(str(x).encode('ascii'))
key = sha1.digest()[:16]

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
flag = cipher.decrypt(ciphertext)
print("Flag:", flag)