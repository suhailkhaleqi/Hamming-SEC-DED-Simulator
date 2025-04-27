import random
import tkinter as tk
from tkinter import messagebox

# Core Functions
def calculate_parity_bits(m):
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def generate_hamming_code(data_bits):
    m = len(data_bits)
    r = calculate_parity_bits(m)
    total_length = m + r + 1
    code = ['0'] * total_length

    j = 0
    for i in range(1, total_length):
        if (i & (i - 1)) != 0:
            code[i] = data_bits[j]
            j += 1

    for i in range(r):
        position = 2 ** i
        parity = 0
        for j in range(1, total_length):
            if j & position:
                parity ^= int(code[j])
        code[position] = str(parity)

    overall_parity = 0
    for bit in code[1:]:
        overall_parity ^= int(bit)
    code[0] = str(overall_parity)

    return ''.join(code)

def introduce_error(codeword, position=None):
    code = list(codeword)
    if position is None:
        position = random.randint(0, len(code) - 1)
    code[position] = '1' if code[position] == '0' else '0'
    return ''.join(code), position

def detect_and_correct(codeword):
    n = len(codeword)
    code = list(codeword)
    r = calculate_parity_bits(n - 1)

    syndrome = 0
    for i in range(r):
        position = 2 ** i
        parity = 0
        for j in range(1, n):
            if j & position:
                parity ^= int(code[j])
        if parity:
            syndrome += position

    computed_overall_parity = 0
    for bit in code[1:]:
        computed_overall_parity ^= int(bit)
    computed_overall_parity ^= int(code[0])

    if syndrome == 0 and computed_overall_parity == 0:
        return ''.join(code), None, "No Error"
    elif syndrome != 0 and computed_overall_parity == 1:
        code[syndrome] = '1' if code[syndrome] == '0' else '0'
        return ''.join(code), syndrome, "Single-bit Error Corrected"
    elif syndrome != 0 and computed_overall_parity == 0:
        return ''.join(code), syndrome, "Double-bit Error Detected (Uncorrectable)"
    else:
        return ''.join(code), None, "Error Detected, Type Unknown"

# GUI
class HammingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming SEC-DED Simülatörü")

        self.memory = []

        tk.Label(root, text="Veri Girişi (8, 16 veya 32 bit)").pack()
        self.data_entry = tk.Entry(root, width=40)
        self.data_entry.pack()

        self.encode_button = tk.Button(root, text="Hamming Kodu Hesapla", command=self.encode_data)
        self.encode_button.pack(pady=5)

        self.result_label = tk.Label(root, text="", fg="blue")
        self.result_label.pack()

        self.introduce_error_button = tk.Button(root, text="Hata Oluştur", command=self.create_error)
        self.introduce_error_button.pack(pady=5)

        self.correct_error_button = tk.Button(root, text="Hata Düzelt", command=self.correct_error)
        self.correct_error_button.pack(pady=5)

        self.memory_listbox = tk.Listbox(root, width=50)
        self.memory_listbox.pack(pady=10)

        self.encoded_data = None
        self.corrupted_data = None

    def encode_data(self):
        data = self.data_entry.get()
        if len(data) not in (8, 16, 32) or not all(bit in '01' for bit in data):
            messagebox.showerror("Hata", "Lütfen 8, 16 veya 32 bitlik doğru bir veri girin (0 ve 1)!")
            return
        self.encoded_data = generate_hamming_code(data)
        self.result_label.config(text=f"Kod: {self.encoded_data}")
        self.memory.append(self.encoded_data)
        self.update_memory()

    def create_error(self):
        if not self.encoded_data:
            messagebox.showerror("Hata", "Önce veri kodlamalısınız!")
            return
        self.corrupted_data, pos = introduce_error(self.encoded_data)
        self.result_label.config(text=f"Hatalı Kod ({pos}. bit): {self.corrupted_data}")

    def correct_error(self):
        if not self.corrupted_data:
            messagebox.showerror("Hata", "Önce hatalı veri oluşturun!")
            return
        corrected, pos, status = detect_and_correct(self.corrupted_data)
        self.result_label.config(text=f"Sonuç: {corrected} ({status})")

    def update_memory(self):
        self.memory_listbox.delete(0, tk.END)
        for item in self.memory:
            self.memory_listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = HammingSimulator(root)
    root.mainloop()
