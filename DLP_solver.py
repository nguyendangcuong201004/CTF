import math  ## Ở bài này em có tham khảo thêm AI  để hiểu cách nó chạy, thì hôm trước anh giảng vậy thì em biết vậy nhưng mà lúc code em gặp nhiều khó khăn

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m

def discrete_log_bsgs(g, a, p):
    n = p - 1
    m = math.isqrt(n) + 1

    table = {}
    e = 1
    for j in range(m):
        if e not in table:
            table[e] = j
        e = (e * g) % p

    inv_gm = modinv(pow(g, m, p), p)
    if inv_gm is None:
        return None

    gamma = a
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * inv_gm) % p

    return None


def factorize(n):
    res = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            res.append((d, cnt))
        d += 1 if d == 2 else 2
    if n > 1:
        res.append((n, 1))
    return res

def crt(rems, mods):
    N = 1
    for m in mods:
        N *= m
    x = 0
    for r, m in zip(rems, mods):
        Ni = N // m
        inv = modinv(Ni, m)
        x = (x + r * Ni * inv) % N
    return x

def pohlig_hellman(g, a, p):
    n = p - 1
    factors = factorize(n)
    rems, mods = [], []

    for q, e in factors:
        xq = 0
        for k in range(e):
            exp = n // (q**(k+1))
            base = pow(g, exp, p)
            rhs = pow(a * pow(g, -xq, p) % p, exp, p)
            y = discrete_log_bsgs(base, rhs, p)
            if y is None:
                return None
            xq += y * (q**k)
        rems.append(xq % (q**e))
        mods.append(q**e)

    return crt(rems, mods) % n


def pollard_rho_dlog(g, h, p, max_steps=500000):
    n = p - 1
    if h == 1:
        return 0

    def f(state):
        x, a, b = state
        if x % 3 == 0:
            x = (x * g) % p
            a = (a + 1) % n
        elif x % 3 == 1:
            x = (x * h) % p
            b = (b + 1) % n
        else:
            x = (x * x) % p
            a = (2 * a) % n
            b = (2 * b) % n
        return x, a, b

    for attempt in range(5): 
        x, a, b = 1, 0, 0
        x_slow, a_slow, b_slow = x, a, b
        x_fast, a_fast, b_fast = f((x, a, b))
        x_fast, a_fast, b_fast = f((x_fast, a_fast, b_fast))

        steps = 0
        while x_slow != x_fast and steps < max_steps:
            x_slow, a_slow, b_slow = f((x_slow, a_slow, b_slow))
            x_fast, a_fast, b_fast = f((x_fast, a_fast, b_fast))
            x_fast, a_fast, b_fast = f((x_fast, a_fast, b_fast))
            steps += 1

        if x_slow != x_fast:
            continue

        r = (a_slow - a_fast) % n
        s = (b_fast - b_slow) % n
        if s == 0:
            continue

        g_ = math.gcd(s, n)
        if r % g_ != 0:
            continue

        r1 = r // g_
        s1 = s // g_
        n1 = n // g_
        inv_s1 = modinv(s1, n1)
        if inv_s1 is None:
            continue

        x_found = (r1 * inv_s1) % n1
        for k in range(g_):
            candidate = (x_found + k * n1) % n
            if pow(g, candidate, p) == h % p:
                return candidate

    return None

def solve(p, g, a, alg="BSGS"):
    alg = alg.lower()
    if alg == "bsgs":
        return discrete_log_bsgs(g, a, p)
    elif alg in ("pohlig-hellman", "pohlighellman", "pohlig"):
        return pohlig_hellman(g, a, p)
    elif alg in ("pollard-rho", "pollard", "rho"):
        return pollard_rho_dlog(g, a, p)
    else:
        raise ValueError("Unknown algorithm. Choose 'BSGS', 'Pohlig-Hellman', or 'Pollard-Rho'.")


if __name__ == "__main__":
    p, g, a = map(int, input("Enter p, g, a: ").split())

    for alg in ("BSGS", "Pohlig-Hellman", "Pollard-Rho"):
        x = solve(p, g, a, alg)
        print(f"{alg}: x = {x}, check = {pow(g, x, p) == a}")
