from pwn import xor
from PIL import Image


lemur = Image.open("lemur.png")
flag = Image.open("flag.png")

lemur_bytes = lemur.tobytes()
flag_bytes = flag.tobytes()

res_bytes = xor(lemur_bytes, flag_bytes)

res_img = Image.frombytes(lemur.mode, lemur.size, res_bytes)

res_img.save("res.png")