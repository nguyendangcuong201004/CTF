import math

def solve_dlp_bsgs(g, a, p):
    """
    Giải bài toán Lôgarit Rời rạc g^x ≡ a (mod p) bằng thuật toán Baby-Step Giant-Step.
    """
    # Bậc của nhóm nhân modulo p
    order = p - 1
    # Tính kích thước bước nhảy lớn, luôn làm tròn lên
    m = math.ceil(math.sqrt(order))

    # --- 1. BABY STEPS ---
    # Nhiệm vụ: Tính a * g^j và lưu vào dictionary
    # Key là kết quả (val), value là số mũ (j)
    baby_steps = {}
    val = a
    for j in range(m):
        baby_steps[val] = j
        val = (val * g) % p

    # --- 2. GIANT STEPS ---
    # Nhiệm vụ: Tính (g^m)^i và tìm xem nó có trong baby_steps không

    # Tính giá trị của một bước nhảy lớn
    giant_step_base = pow(g, m, p)
    
    # Bắt đầu với bước nhảy lớn đầu tiên (i=1)
    giant_val = giant_step_base
    for i in range(1, m + 1):
        # Kiểm tra xem có "gặp nhau ở giữa" không
        if giant_val in baby_steps:
            # Nếu có, lấy ra giá trị j tương ứng
            j = baby_steps[giant_val]
            
            # Công thức quan trọng nhất, rất dễ sai ở đây!
            x = (i * m - j + order) % order
            
            # Kiểm tra lại nghiệm để đảm bảo 100% đúng
            if pow(g, x, p) == a:
                return x
        
        # Di chuyển đến bước nhảy lớn tiếp theo
        giant_val = (giant_val * giant_step_base) % p
        
    # Nếu chạy hết vòng lặp mà không tìm thấy
    return None

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == '__main__':
    g_input = 6
    a_input = 248
    p_input = 457

    print(f"Bắt đầu giải bài toán: {g_input}^x ≡ {a_input} (mod {p_input})")
    
    solution_x = solve_dlp_bsgs(g_input, a_input, p_input)

    if solution_x is not None:
        print(f"✅ Tìm thấy nghiệm! x = {solution_x}")
    else:
        print("❌ Không tìm thấy nghiệm cho bài toán.")