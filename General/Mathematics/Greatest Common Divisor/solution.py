#Thuật toán Euclid để tìm UCLN
# gcd (a, b) = gcd (b, a % b)


def gcd_euclid(a, b):
    if b > a:
        a, b = b, a
    
    while b != 0:
        a, b = b, a % b
    return  a


def gcd_euclid_recur(a, b):
    if b == 0:
        return a
    return gcd_euclid_recur(b, a % b)

print (gcd_euclid(66528, 52920))
print (gcd_euclid_recur(66528, 52920))